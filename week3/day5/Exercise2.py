import requests

# # Retrieve a random chuck joke in JSON format.
# response = requests.get("https://api.chucknorris.io/jokes/random")
# print (response.json())

# # Retrieve a list of available categories.
# response = requests.get("https://api.chucknorris.io/jokes/categories")
# print (response.json())

# Retrieve a random chuck norris joke from a given category.
category = "animal"
response = requests.get("https://api.chucknorris.io/jokes/random?category={category}")
print (response.json())

