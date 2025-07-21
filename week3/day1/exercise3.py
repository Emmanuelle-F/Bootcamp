# Exercise
# Given a list of numbers, write a function that returns the sum of every number. BUT you can have a malicious string inside the list.

my_list = [2,3,1,2,"four",42,1,5,3,"imanumber"]

def sumNumbers(numbersList):
    sum = 0

    for number in numbersList:
        try:
            number = int(number)
            sum += number

        except:
            continue

    return sum

print(f"{sumNumbers(my_list)}")


#     try:
#         for number in numbersList:
#             number = int(number)
#             sum += number
#         return sum

#     except:
#         print("number not found")

# print(f"{sumNumbers(my_list)}")
