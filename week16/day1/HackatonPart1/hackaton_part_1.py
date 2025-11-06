import asyncio
import json
import textwrap
import time
import streamlit as st

from tavily import AsyncTavilyClient
from llama_index.core.workflow import Context
from llama_index.core.tools import FunctionTool
from llama_index.core.agent.workflow import (
    FunctionAgent,
    AgentWorkflow,
    AgentInput,
    AgentOutput,
    ToolCall,
    ToolCallResult,
    AgentStream,
)
from llama_index.llms.groq import Groq

GROQ_API_KEY = ""
TAVILY_API_KEY = ""
MODEL_NAME = "openai/gpt-oss-120b"   #  llama-3.1-70b-versatile   openai/gpt-oss-120b

st.set_page_config(page_title="Multi-Agent LinkedIn Blog Writing System", page_icon="✍️", layout="wide")
st.title("✍️ Multi-Agent LinkedIn Blog Writing System")

# Prompt
default_prompt = (
    "Write me a blog post on generative AI of about 80 words. "
    "Briefly describe the history of generative AI and some examples."
)
user_prompt = st.text_area("📝 Prompt", value=default_prompt, height=120)

# Layout placeholders
col1, col2 = st.columns([1.2, 1])
with col1:
    log_box = st.empty()          # event log
with col2:
    notes_box = st.empty()        # research notes
    blog_box = st.empty()         # blog markdown
    review_box = st.empty()       # review text


# Web search tool (async) — now with error surfacing
async def web_search(query: str, recency_days: int = None, top_n: int = 5, **kwargs) -> str:
    """Useful for using the web to answer questions."""
    try:
        client = AsyncTavilyClient(api_key=TAVILY_API_KEY)
        result = await client.search(query, search_depth="basic", max_results=top_n)
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        return f"ERROR: web_search failed -> {type(e).__name__}: {e}"

# Notes tool (async)
async def record_notes(ctx: Context, notes: str, notes_title: str) -> str:
    """Record notes on a given topic. Provide notes and a title."""
    try:
        async with ctx.store.edit_state() as ctx_state:
            if "research_notes" not in ctx_state["state"]:
                ctx_state["state"]["research_notes"] = {}
            ctx_state["state"]["research_notes"][notes_title] = notes
        return "Notes recorded."
    except Exception as e:
        return f"ERROR: record_notes failed -> {type(e).__name__}: {e}"

# Blog writer tool (async)
async def blog_writer(ctx: Context, blog_content: str) -> str:
    """Write a markdown blog post on a given topic."""
    try:
        async with ctx.store.edit_state() as ctx_state:
            ctx_state["state"]["blog_content"] = blog_content
        return "Blog written."
    except Exception as e:
        return f"ERROR: blog_writer failed -> {type(e).__name__}: {e}"

# Review tool (async)
async def review_blog(ctx: Context, review: str) -> str:
    """Review a blog post and suggest improvements."""
    try:
        async with ctx.store.edit_state() as ctx_state:
            ctx_state["state"]["review"] = review
        return "Blog reviewed."
    except Exception as e:
        return f"ERROR: review_blog failed -> {type(e).__name__}: {e}"

def build_tools():
    return (
        FunctionTool.from_defaults(
            fn=web_search,
            name="web_search_tool",
            description="Useful for using the web to answer questions.",
        ),
        FunctionTool.from_defaults(
            fn=record_notes,
            name="record_notes_tool",
            description="Record notes on a given topic. Provide notes and a title.",
        ),
        FunctionTool.from_defaults(
            fn=blog_writer,
            name="write_blog_tool",
            description="Write a markdown blog post on a given topic.",
        ),
        FunctionTool.from_defaults(
            fn=review_blog,
            name="review_blog_tool",
            description="Review a blog post and suggest improvements.",
        ),
    )

def build_agents(llm, tools):
    web_search_tool, record_notes_tool, write_blog_tool, review_blog_tool = tools

    research_agent = FunctionAgent(
        name="ResearchAgent",
        description="Search the web for information and record notes.",
        system_prompt=(
            "You are the ResearchAgent that can search the web for information on a given topic and record notes. "
            "Once notes are recorded and you are satisfied, hand off to the WriteAgent to write the blog post. "
            "Have at least some notes before handing off."
        ),
        llm=llm,
        tools=[web_search_tool, record_notes_tool],
        can_handoff_to=["WriteAgent"],
    )

    write_agent = FunctionAgent(
        name="WriteAgent",
        description="Write a blog post on a given topic.",
        system_prompt=(
            "You are the WriteAgent that writes a blog post in markdown. Ground your writing in the research notes. "
            "After writing the blog post, you MUST immediately hand off to the ReviewAgent for feedback. "
            "If the ReviewAgent requests changes, implement them and then hand back for a final review."
        ),
        llm=llm,
        tools=[write_blog_tool],
        can_handoff_to=["ReviewAgent", "ResearchAgent"],
    )

    review_agent = FunctionAgent(
        name="ReviewAgent",
        description="Review a blog post and suggest improvements.",
        system_prompt=(
            "You are the ReviewAgent that reviews the blog and suggests improvements. "
            "Write a concise, actionable review. If changes are required, explicitly hand back to the WriteAgent. "
            "If the post is good to publish, clearly state that it is approved."
        ),
        llm=llm,
        tools=[review_blog_tool],
        can_handoff_to=["WriteAgent"],
    )

    return research_agent, write_agent, review_agent

def build_workflow(research_agent, write_agent, review_agent):
    return AgentWorkflow(
        agents=[research_agent, write_agent, review_agent],
        root_agent=research_agent.name,
        initial_state={
            "research_notes": {},
            "blog_content": "Not written yet.",
            "review": "Review required.",
        },
    )


async def run_agents_and_stream(prompt: str):
    """Runs the workflow and streams events to Streamlit placeholders."""
    llm = Groq(model=MODEL_NAME, api_key=GROQ_API_KEY, additional_kwargs={"tool_choice": "auto"})
    tools = build_tools()
    research_agent, write_agent, review_agent = build_agents(llm, tools)
    agent_workflow = build_workflow(research_agent, write_agent, review_agent)

    latest_notes = {}
    latest_blog_md = None
    latest_review = None

    rolling_text_by_agent = {}

    logs = []
    current_agent = None

    handler = agent_workflow.run(user_msg=prompt)
    got_any_event = False

    async for event in handler.stream_events():
        got_any_event = True

        # Agent switch
        if hasattr(event, "current_agent_name"):
            current_agent = event.current_agent_name
            logs.append("\n" + "=" * 50)
            logs.append(f"🤖 Agent: {current_agent}")
            logs.append("=" * 50 + "\n")
            rolling_text_by_agent.setdefault(current_agent, "")


        if isinstance(event, AgentStream):
            if getattr(event, "delta", None):
                rolling_text_by_agent[current_agent] = rolling_text_by_agent.get(current_agent, "") + str(event.delta)
                logs.append(f"… {textwrap.shorten(str(event.delta), width=140, placeholder=' …')}")

        elif isinstance(event, AgentOutput):
            if event.response and event.response.content:
                logs.append(f"📤 Output: {event.response.content}")
                rolling_text_by_agent[current_agent] = rolling_text_by_agent.get(current_agent, "") + str(event.response.content)
                if current_agent == "ReviewAgent":
                    latest_review = event.response.content
            if event.tool_calls:
                tools_list = [call.tool_name for call in event.tool_calls]
                logs.append(f"🛠️ Planning to use tools: {tools_list}")

        elif isinstance(event, ToolCall):
            logs.append(f"🔨 Calling Tool: {event.tool_name}")
            logs.append(f"  With arguments: {event.tool_kwargs}")

        elif isinstance(event, ToolCallResult):
            logs.append(f"🔧 Tool Result ({event.tool_name}):")
            pretty_args = textwrap.shorten(str(event.tool_kwargs), width=500, placeholder=" …")
            logs.append(f"  Arguments: {pretty_args}")
            try:
                out_txt = str(event.tool_output)
            except Exception as e:
                out_txt = f"<non-stringable output: {type(e).__name__}: {e}>"
            short_out = textwrap.shorten(out_txt, width=800, placeholder=" …")
            logs.append(f"  Output: {short_out}")


            if event.tool_name == "record_notes_tool":
                try:
                    notes = event.tool_kwargs.get("notes", "")
                    title = event.tool_kwargs.get("notes_title", "Notes")
                    latest_notes[title] = notes
                except Exception:
                    pass
            elif event.tool_name == "write_blog_tool":
                latest_blog_md = event.tool_kwargs.get("blog_content", "")
            elif event.tool_name == "review_blog_tool":
                latest_review = event.tool_kwargs.get("review", "")

        log_box.markdown("```\n" + "\n".join(logs[-200:]) + "\n```")
        if latest_notes:
            last_title = list(latest_notes.keys())[-1]
            notes_box.markdown(f"### 🗒️ Research Notes ({last_title})\n\n```\n{latest_notes[last_title]}\n```")
        if latest_blog_md is not None:
            blog_box.markdown("### 🧾 Blog Draft\n\n" + latest_blog_md)
        if latest_review is not None:
            review_box.markdown("### ✅ Review\n\n" + f"> {latest_review}")

    write_text = rolling_text_by_agent.get("WriteAgent", "").strip()
    review_text = rolling_text_by_agent.get("ReviewAgent", "").strip()

    if not latest_review and review_text:
        review_box.markdown("### ✅ Review (from stream)\n\n" + f"> {review_text}")

# Run Button
if st.button("▶️ Run Agents", type="primary"):
    if not user_prompt.strip():
        st.error("Please enter a prompt to run.")
    else:
        # Reset panels
        log_box.empty()
        notes_box.empty()
        blog_box.empty()
        review_box.empty()

        try:
            asyncio.run(run_agents_and_stream(user_prompt.strip()))
        except RuntimeError as e:
            if "asyncio.run() cannot be called from a running event loop" in str(e):
                loop = asyncio.get_event_loop()
                loop.create_task(run_agents_and_stream(user_prompt.strip()))
            else:
                st.exception(e)
