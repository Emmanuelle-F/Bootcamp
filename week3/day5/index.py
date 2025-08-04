import json

jsonFile = r'C:\Users\emmaf\Documents\Bootcamp\week3\day5\file.json'

# Load data from file.json into the variable `family`
with open(jsonFile, 'r') as fileObject:
    family = json.load(fileObject)

# Print nicely the details about Jane's children
for child in family["children"]:
    print(f"Name: {child['firstName']} Age: {child['age']}")

# Add favorite_color to each child
family["children"][0]["favoriteColor"] = "purple"
family["children"][1]["favoriteColor"] = "blue"


# Then, save back all the new data into the json file
with open(jsonFile, 'w') as fileObject:
    json.dump(family, fileObject)

# Use the indent argument inside the dump function.
with open(jsonFile, 'w') as fileObject:
    json.dump(family, fileObject, indent = 2)




print(family)