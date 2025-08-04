# Read the file line by line
for line in open(r'C:\Users\emmaf\Documents\Bootcamp\week3\day5\namesList.txt'):
    print(line)


# Read only the 5th line of the file
for i, line in enumerate(open(r'C:\Users\emmaf\Documents\Bootcamp\week3\day5\namesList.txt')):
    if i == 4:
        print(line)
    

# Read only the 5 first characters of the file
with open (r'C:\Users\emmaf\Documents\Bootcamp\week3\day5\namesList.txt', 'r') as f:
    print(f.readline(5))


# Read all the file and return it as a list of strings. Then split each word
stringList = []
for line in open(r'C:\Users\emmaf\Documents\Bootcamp\week3\day5\namesList.txt'):
    stringList.append(line.strip())
print(stringList)


# Find out how many occurences of the names "Darth", "Luke" and "Lea" are in the file
# Append your first name at the end of the file
# Append "SkyWalker" next to each first name "Luke"