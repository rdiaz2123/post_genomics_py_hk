#Ricardo Diaz 
#Homework 1 
#Post Genomics 


#Part 2.1 
#Create own function that reads two matrices (list or df) that 
#returns the product of these two 

#I will be assuming that the matrices will be in the following format: 

# example x_list = [[3, 41, 4]
#                   [5, 7, 8]
#                   [45, 6, 2]]

#   b_list = [[ 8, 1]
#             [ 9, 3]
#             [ 0, 4]]

#where x_list is a 3 x 3 matrix (row x col)
#and b_list is a 3 x 2 matrix (row x col)

#Where x_list first row is 3 , 41, 4 and its first col is 
#that of 3 , 5 , 45 

matrix_1 = [[3, 41, 4],
            [5, 7, 8],
            [45, 6, 2]]

matrix_2 = [[8, 1],
            [9, 3],
            [0, 4]]

matrix_3 = [[0, 2, 1],
            [3, 4, 3],
            [4, 5, 9]]

matrix_4 = [[1, 2, 1],
            [3, 6, 8],
            [0, 1, 0]]



# print(matrix_1)
# len(matrix_1[0])
# len(matrix_1)

#in order to multiply matrices we need to have the following rule 
#in mind which is that of the number of col in the frist matrix 
#must equal the number of rows in matrix B 

def two_matrix_mult(list_1, list_2): 
    if len(list_1[0]) == len(list_2):
        
        final_matrix = [[0 for i in range(len(list_2[0]))] for i in range(len(list_1))]
        #what the line above does is that it will initialize an empty 
        #final matrix and it will be filled with zeros, so for example if 
        #the first matrix is a 3 x 3 and the second is a 3 x 2 this line will create 
        #the final result that needs to be the 3 x 2 

        for r in range(len(list_1)):
            for k in range(len(list_2[0])):
                for m in range(len(list_2)):
                    final_matrix[r][k] += list_1[r][m] * list_2[m][k]

        #what the lines above do is that in the first loop it is going to iterate through each row of the frist matrix 
        #the second loop iterates through each col of the second matrix 
        #the third loop iterates m over each element in row r of the first matrix and col k of the second matrix 
        #the final line add the computed dot product of rows and cols

        #finally the final product matrix will be returned
        return final_matrix
    else:
        return "The matrices you are trying to multiply does not follow the dot product rule, therefore it is not applicable."


problem_1 = two_matrix_mult(matrix_1, matrix_2)
print(problem_1)
problem_2 = two_matrix_mult(matrix_1, matrix_3)
print(problem_2)
problem_3 = two_matrix_mult(matrix_2, matrix_3)
print(problem_3)

#part 2.2 

import numpy as np 

matrix_1_numpy = [[3, 41, 4],
            [5, 7, 8],
            [45, 6, 2]]

matrix_2_numpy = [[8, 1],
            [9, 3],
            [0, 4]]

first_mat = np.array(matrix_1_numpy)
second_mat = np.array(matrix_2_numpy)

numpy_dot_product = np.dot(first_mat, second_mat)

print(numpy_dot_product)

import time 
#first function to test time 
start_time = time.perf_counter()
problem_1 = two_matrix_mult(matrix_1, matrix_2)
end_time = time.perf_counter() 

elapsed_time = end_time - start_time
print(elapsed_time)

#second function to test time 
start_time_2 = time.perf_counter()
problem_1 = two_matrix_mult(matrix_1, matrix_2)
end_time_2 = time.perf_counter() 

elapsed_time_2 = end_time_2 - start_time_2
print(elapsed_time_2)

#Well from my results running the code above the faster method was that from 
#numpy but not by a lot but a lot in the coding world. My function can be shortened down 
#to a better coding standard where optimazation can be done by the way one writes code in 
#order to consume less memory. 