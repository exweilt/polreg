import math
import random
import copy
from typing import Tuple

import utils

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
        error = 0
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