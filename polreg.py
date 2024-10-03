import math
import random
import copy
from typing import Tuple

import utils

def gradient_descent(points, learning_rate=0.01, num_iterations=1000):
    """
    Performs gradient descent to find the coefficients a and b for y = ax + b.

    :param points: A list of tuples, where each tuple is (x, y).
    :param learning_rate: The learning rate for gradient descent.
    :param num_iterations: The number of iterations to perform.
    :return: The coefficients a and b.
    """
    # Initialize coefficients
    a = 0.0  # slope
    b = 0.0  # intercept

    n = len(points)  # Number of data points

    for _ in range(num_iterations):
        # Initialize gradients
        gradient_a = 0.0
        gradient_b = 0.0

        # Calculate gradients
        for x, y in points:
            prediction = a * x + b
            error = prediction - y
            gradient_a += (2 / n) * error * x  # Partial derivative w.r.t a
            gradient_b += (2 / n) * error        # Partial derivative w.r.t b

        # Update coefficients
        a -= learning_rate * gradient_a
        b -= learning_rate * gradient_b

    return a, b

class PolynomialRegression:
    coeff_letter_binding = ["a", "b", "c", "d", "e", "f"]

    # degree: int -> Degree of polynomial
    # coefs: list[float] -> Starting coefficients of the polynomial
    # points: list[Tuple[float, float]] = [] -> points of data
    def __init__(self, degree: int, coefs: list[float], points: list[Tuple[float, float]] = []) -> None:
        assert len(coefs) == degree+1
        
        self.degree = degree
        self.coefficients = coefs
        self.points = points

    def predict(self, x: float):
        y = 0
        for term_idx in range(self.degree + 1):
            y += self.coefficients[term_idx] * pow(x, self.degree - term_idx)
        
        return y
    
    def loss(self):
        error = 0.0
        for p in self.points:
            error += pow(self.predict(p[0]) - p[1], 2)
        return error
    
    def get_polynomial_string(self) -> str:
        result = ""
        for term_idx in range(self.degree + 1):
            power = self.degree - term_idx

            # write the sign
            if self.coefficients[term_idx] < 0:
                result += " - " if term_idx > 0 else " -"
            elif term_idx > 0:
                result += " + "

            if power == 1:
                result += f"{abs(self.coefficients[term_idx]):.3g}x"
            elif power == 0:
                result += f"{abs(self.coefficients[term_idx]):.3g}"
            else:
                result += f"{abs(self.coefficients[term_idx]):.3g}x^{power}"
            
        
        return result
    
    # Training based on pure random.
    # Generating many many different functions and pick the best one.
    # Extremely unefficient yet simple and straightforward.
    def train_complete_shuffle(self, num_iter: int = 100):
        best_loss = self.loss()
        best_coeffs = copy.deepcopy(self.coefficients)

        if self.degree != 1:
            print("Error. Works for 1st degree only now")
            exit()
        
        coeff_range_a = (-10, 10)
        coeff_range_b = (-1000, 1000)

        for i in range(num_iter):
            self.coefficients[0] = random.uniform(coeff_range_a[0], coeff_range_a[1])
            self.coefficients[1] = random.uniform(coeff_range_b[0], coeff_range_b[1])
            # for j in range(self.degree + 1):
            #     self.coefficients[j] = random.uniform(coeff_range[0], coeff_range[1])
            new_loss = self.loss()
            if new_loss < best_loss:
                print(f"i({i}) New Loss reached: {new_loss} with coeffs a={self.coefficients[0]} b={self.coefficients[1]}")
                best_loss = new_loss
                best_coeffs = copy.deepcopy(self.coefficients)

        self.coefficients = best_coeffs

        print(f"Training finished. Best loss: { self.loss() }")

    # Returns history of coefficients change
    def train_gradient_descent(self, num_iter: int = 100) -> list[list[float]]:
        assert self.degree == 1 # only 1st degree now

        LEARNING_RATE = 0.00000001
        STEP_SIZE = 0.000001

        for iter_idx in range(num_iter):
            loss = self.loss()

            # Gradient for b
            mutated_coeffs_b = copy.deepcopy(self.coefficients)
            mutated_coeffs_b[1] += STEP_SIZE
            new_loss = PolynomialRegression(self.degree, mutated_coeffs_b, self.points).loss()
            Grad_b = (new_loss - loss) / STEP_SIZE

            # Gradient for a
            mutated_coeffs_a = copy.deepcopy(self.coefficients)
            mutated_coeffs_a[0] += STEP_SIZE
            new_loss = PolynomialRegression(self.degree, mutated_coeffs_a, self.points).loss()
            Grad_a = (new_loss - loss) / STEP_SIZE

            # Mutate
            self.coefficients[0] -= Grad_a * LEARNING_RATE
            self.coefficients[1] -= Grad_b * LEARNING_RATE

            print(f"Iteration {iter_idx} finished. New Loss = {self.loss()}")
            print(f"a = {self.coefficients[0]}, b = {self.coefficients[1]} \n")
