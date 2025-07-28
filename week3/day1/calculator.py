# once by importing the whole module

import operators

addition = operators.addOperator(5,5)
print(addition)

division = operators.divideOperator(6,2)
print(division)

###########################################################
# the second time by importing specific functions

from operators import addOperator, divideOperator

addition = addOperator(5,5)
print(addition)

division = divideOperator(6,2)
print(division)

###########################################################
# the third time by using alias

from operators import addOperator as add, divideOperator as div

addition = add(5,5)
print(addition)

division = div(6,2)
print(division)













# Create another file called calculator.py, and import the operators module. Call the 2 functions and display the results

# Do this process 3 times :

# once by importing the whole module
# the second time by importing specific functions
# the third time by using alias