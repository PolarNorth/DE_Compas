"""Backend for solving differential equations
"""
import math

_eps = 9

class NumericalMethod:
    """Interface for numerical methods
    """
    @classmethod
    def solve(cls, dif_eq, x0, y0, h, xb):
        pass

    @classmethod
    def _truncation_error(dif_eq, x0, y0, h, xb):
        pass



class DifferentialEquation:
    """Interface for differential equations
    """
    def __init__(self, function, name, exact_solution):
        self.function = function
        self.name = name
        self.exact_solution = exact_solution

    def function(x):
        return self.function(x)
    
    def get_str_name():
        return self.name
    
    def analytical_soluton(x):
        return self.exact_solution(x)

class Solution:
    """Class representing solution of differential equation
       using numerical method
    """
    def __init__(self, x_solution, y_solution, x_error, y_error, x_exact, y_exact, str_name):
        self.x_solution = x_solution
        self.y_solution = y_solution
        self.x_error = x_error
        self.y_error = y_error
        self.x_exact = x_exact
        self.y_exact = y_exact
        self.str_name = str_name

class EulerMethod (NumericalMethod):
    @classmethod
    def solve(cls, diff_eq, y0, x0, xb, h):
        f = diff_eq.function
        x = [x0]
        y = [y0]
        curr_x = x0
        curr_y = y0
        while curr_x < xb:
            # print("curr_y = {} + {} * {}".format(curr_y,h,f(curr_x, curr_y)))
            curr_y = curr_y + h * f(curr_x, curr_y)
            curr_x = curr_x + h
            curr_x = round(curr_x, cls._eps)
            x.append(curr_x)
            y.append(curr_y)
            # print("{} -> {};".format(curr_x, curr_y))
        return x,y

class ImprovedEulerMethod (NumericalMethod):
    @classmethod
    def solve(cls, diff_eq, y0, x0, xb, h):
        f = diff_eq.function
        x = [x0]
        y = [y0]
        curr_x = x0
        curr_y = y0
        while curr_x < xb:
            # print("curr_y = {} + {} * {}".format(curr_y,h,f(curr_x, curr_y)))
            curr_y = curr_y + h * f(curr_x + h/2, curr_y + h/2 * f(curr_x, curr_y))
            curr_x = curr_x + h
            curr_x = round(curr_x, _eps)
            x.append(curr_x)
            y.append(curr_y)
            # print("{} -> {};".format(curr_x, curr_y))
        # return x,y
        return Solution(x, y, [], [], [], [], diff_eq.name)

class RungeKuttaMehod (NumericalMethod):
    @classmethod
    def solve(cls, diff_eq, y0, x0, xb, h):
        f = diff_eq.function
        x = [x0]
        y = [y0]
        curr_x = x0
        curr_y = y0
        while curr_x < xb:
            # print("curr_y = {} + {} * {}".format(curr_y,h,f(curr_x, curr_y)))
            k1 = f(curr_x, curr_y)
            k2 = f(curr_x + h/2, curr_y + h*k1/2)
            k3 = f(curr_x + h/2, curr_y + h*k2/2)
            k4 = f(curr_x + h, curr_y + h*k3)
            delta_y = h * (k1 + 2*k2 + 2*k3 + k4) / 6
            curr_y = curr_y + delta_y
            curr_x = curr_x + h
            curr_x = round(curr_x, cls._eps)
            x.append(curr_x)
            y.append(curr_y)
            # print("{} -> {};".format(curr_x, curr_y))
        return x,y

equations = [
    DifferentialEquation(lambda x,y : x*x - 3*x*y + y*y - 3*y, "test", (lambda x : x + 5))
]