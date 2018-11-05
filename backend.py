"""Backend for solving differential equations
"""
import math


class NumericalMethod:
    """Base class for numerical methods
    """
    _eps = 9

    def solve(self, dif_eq, x0, y0, h, xb): # TODO : Probably it is better to calculate x inside this function and use in calls
        # print("x0={}, y0={}, h={}, xb={}".format(str(x0), str(y0), str(h), str(xb)))
        x_solution, y_solution = self._get_numerical_solution(dif_eq, x0, y0, h, xb)
        x_exact, y_exact = self._get_exact_solution(dif_eq, x_solution)
        x_error, y_error = self._get_truncation_error(x_solution, y_solution, y_exact)
        return Solution(x_solution, y_solution, x_error, y_error, x_exact, y_exact, dif_eq.get_str_name(), self.get_method_name())

    def _get_truncation_error(self, x, y_solution, y_exact):
        y_error = []
        for idx in range(0,len(x)):
            y_error.append(abs(y_exact[idx] - y_solution[idx]))
        return x, y_error
    
    def _get_exact_solution(self, dif_eq, x_solution):
        y = []
        for x in x_solution:
            y.append(dif_eq.exact_solution(x))
        return x_solution, y
    
    def _get_numerical_solution(self, dif_eq, x0, y0, h, xb):
        pass
    
    def get_method_name(self):
        pass


class DifferentialEquation:
    """Interface for differential equations
    """
    def __init__(self, function, name, exact_solution):
        self.function = function
        self.name = name
        self.exact_solution = exact_solution

    def function(self, x):
        return self.function(x)
    
    def get_str_name(self):
        return self.name
    
    def analytical_soluton(self, x):
        return self.exact_solution(x)

class Solution:
    """Class representing solution of differential equation
       using numerical method
    """
    def __init__(self, x_solution, y_solution, x_error, y_error, x_exact, y_exact, str_name, str_method_name):
        self.x_solution = x_solution
        self.y_solution = y_solution
        self.x_error = x_error
        self.y_error = y_error
        self.x_exact = x_exact
        self.y_exact = y_exact
        self.str_name = str_name
        self.str_method_name = str_method_name    

class EulerMethod (NumericalMethod):
    def _get_numerical_solution(self, diff_eq, x0, y0, h, xb):
        f = diff_eq.function
        x = [x0]
        y = [y0]
        curr_x = x0
        curr_y = y0
        while curr_x < xb:
            # print("curr_y = {} + {} * {}".format(curr_y,h,f(curr_x, curr_y)))
            curr_y = curr_y + h * f(curr_x, curr_y)
            curr_x = curr_x + h
            curr_x = round(curr_x, self._eps)
            x.append(curr_x)
            y.append(curr_y)
            # print("{} -> {};".format(curr_x, curr_y))
        return x,y
        
    def get_method_name(self):
        return "Euler"

class ImprovedEulerMethod (NumericalMethod):
    def _get_numerical_solution(self, diff_eq, x0, y0, h, xb):
        f = diff_eq.function
        x = [x0]
        y = [y0]
        curr_x = x0
        curr_y = y0
        while curr_x < xb:
            # print("curr_y = {} + {} * {}".format(curr_y,h,f(curr_x, curr_y)))
            curr_y = curr_y + h * f(curr_x + h/2, curr_y + h/2 * f(curr_x, curr_y))
            curr_x = curr_x + h
            curr_x = round(curr_x, self._eps)
            x.append(curr_x)
            y.append(curr_y)
            # print("{} -> {};".format(curr_x, curr_y))
        return x,y
        
    def get_method_name(self):
        return "Improved Euler"

class RungeKuttaMethod (NumericalMethod):
    def _get_numerical_solution(self, diff_eq, x0, y0, h, xb):
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
            curr_x = round(curr_x, self._eps)
            x.append(curr_x)
            y.append(curr_y)
            # print("{} -> {};".format(curr_x, curr_y))
        return x,y
        
    def get_method_name(self):
        return "Runge-Kutta"
    

equations = [
    # DifferentialEquation(lambda x,y : x*x - 3*x*y + y*y - 3*y, "test", (lambda x : x + 5)),
    DifferentialEquation(lambda x,y : -x + y * (2*x + 1) / x, "-x + y(2x + 1)/x", (lambda x : x * (1 + 5 * math.exp(2*x - 2)) / 2))
]

numerical_methods = {
    "Euler" : EulerMethod(),
    "Improved Euler" : ImprovedEulerMethod(),
    "Runge-Kutta" : RungeKuttaMethod(),
}