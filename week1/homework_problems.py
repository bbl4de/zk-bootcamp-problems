import numpy as np

# Problem 1 : congruent values
p = 71

arr = [-1, -4, -160, 500]

print("Problem 1 : congruent values")
def find_congruent_value_in_p(x, p): 
    for i in x:
        print(pow(i, -1, p))

find_congruent_value_in_p(arr, p)

# Problem 2: check assertion of congruent values after finding their inverses

a = 5/6 
b = 11/12
c = 21/12

a_inverse = pow(6, -1, p)
b_inverse = pow(12, -1, p)
c_inverse = pow(12, -1, p)

a_c = (5 * a_inverse) % p
b_c = (11 * b_inverse) % p
c_c = (21* c_inverse) % p

# even that addition is over the prime field! 
assert((a_c + b_c) % p == c_c)

# Problem 3: sum of congruent values after finding their inverses

a = 2/3
b = 1/2
c = 1/3

a_inverse = pow(3, -1, p)
b_inverse = pow(2, -1, p)
c_inverse = pow(3, -1, p)

a_c = (2 * a_inverse) % p
b_c = (1 * b_inverse) % p
c_c = (1 * c_inverse) % p

assert((a_c * b_c) % p == c_c)

# Problem 4: Inverse of a matrix
A = np.array([[1, 1], [1, 4]])

# Easier way usign numpy
A_inv = np.linalg.inv(A)

assert(np.allclose((A @ A_inv) % p, np.eye(2)))

# Intended way from the homework - inverse of the determinent times the adjugate of the matrix
det_A = ((1 * 4 ) % p - (1 * 1 ) % p) % p
# Inverse of that determinant
det_A_inv = pow(det_A, -1, p)
# Adjugate of the matrix
A_adjugate = np.array([[4, -1], [-1, 1]])

A_inverse_manual = np.array([[4 * det_A_inv % p, -1 * det_A_inv % p],
                              [-1 * det_A_inv % p, 1 * det_A_inv % p]])
assert(np.allclose((A @ A_inverse_manual) % p, np.eye(2)))