import numpy as np
import galois
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

assert(np.allclose((A @ A_inv) % p, np.identity(2)))

# Intended way from the homework - inverse of the determinent times the adjugate of the matrix
det_A = ((1 * 4 ) % p - (1 * 1 ) % p) % p
# Inverse of that determinant
det_A_inv = pow(det_A, -1, p)
# Adjugate of the matrix
A_adjugate = np.array([[4, -1], [-1, 1]])

A_inverse_manual = np.array([[4 * det_A_inv % p, -1 * det_A_inv % p],
                              [-1 * det_A_inv % p, 1 * det_A_inv % p]])
assert(np.allclose((A @ A_inverse_manual) % p, np.identity(2)))

# Problem 5: Modular square root of 12 - brute force method

def modular_square_root(n, p):
    for x in range(p):
        if (x * x) % p == n:
            return x
    return None

print(modular_square_root(12, p))

# Problem 6: calculate p(x)+q(x) and p(x)*q(x) for polynomials p(x) and q(x) using galois

p_x = galois.Poly([52, 24 ,61], field=galois.GF(p))
q_x = galois.Poly([40, 40, 58], field=galois.GF(p))

def add_polynomials(p_x, q_x):
    return p_x + q_x

def multiply_polynomials(p_x, q_x):
    return p_x * q_x    

# find roots using galois
def find_roots_of_polynomial(poly):
    roots = poly.roots()
    return roots

print(add_polynomials(p_x, q_x))
print(multiply_polynomials(p_x, q_x))
print(find_roots_of_polynomial(p_x))
print(find_roots_of_polynomial(q_x))
print(find_roots_of_polynomial(multiply_polynomials(p_x, q_x)))

# Problem 7: lagrangian interpolation
point1 = (10, 15)
point2 = (23, 29)

def lagrangian_interpolation(points):
    x_values = [point[0] for point in points]
    y_values = [point[1] for point in points]
    
    def L(k, x):
        product = 1
        for i, x_i in enumerate(x_values):
            if i != k:
                product *= (x - x_i) / (x_values[k] - x_i)
        return product
    
    def P(x):
        return sum(y_values[k] * L(k, x) for k in range(len(points)))
    
    return P

assert(lagrangian_interpolation([point1, point2])(10), 15)  # Should return 15
assert(lagrangian_interpolation([point1, point2])(23), 29)  # Should return 29

# problem 8 : interpolate three points with galois
# Create the prime-field GF(71)
GF = galois.GF(71)

# Sample points  (x_i, y_i)
x = GF([0, 1, 2])
y = GF([1, 2, 1])

# Interpolate: returns a galois.Poly instance over GF(71)
f = galois.lagrange_poly(x, y)

print("polynomial: ", f)

assert np.array_equal(f(x), y)