import numpy as np


matrix = np.array([[.5,.5,0,0],
		  [.5,.5,0,0],
		  [.25,.25,.25,.25],
		  [0,0,0,1]])

matrix_transpose = matrix.T
matrix_transpose_sub = matrix_transpose - np.eye(4)
newrow = [1,1,1,1]

matrix_transpose_sub_new_row = np.vstack([matrix_transpose_sub, newrow])


B = np.array([0,0,0,0,1])
B = np.expand_dims(np.array(B),-1)
print(B)


A = np.dot(matrix_transpose_sub_new_row.T,matrix_transpose_sub_new_row)
B = np.dot(matrix_transpose_sub_new_row.T,B)

results = np.linalg.solve(A,B)

