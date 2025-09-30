import numpy as np

matrix1 = np.arange(1,10).reshape(3,3)
matrix2 = np.arange(1,10).reshape(3,3)

print ("Matrix1: \n", matrix1)
print ("Matrix2: \n", matrix2)

matrix_sum = np.add(matrix1, matrix2)
matrix_diff = np.subtract(matrix1, matrix2)
matrix_mult = np.dot(matrix1, matrix2)

print ("Addition: \n", matrix_sum)
print ("Subtraction: \n", matrix_diff)
print ("Multiplication: \n", matrix_mult)