from typing import Any, Callable

import numpy as np
import numbers
import math


# Class for random variable. Can take any function that generates random numbers. Parameters for that function
# must be passed through **rv_parameters. Can also generate
class RandomVariable:
    def __init__(self, rng_func, **rv_parameters):
        assert callable(rng_func)

        # Save the parameters to be used upon calling generate
        self.__parameters = rv_parameters
        # Save the original function
        self.__starting_rng_func = rng_func
        # Set the rng function
        self.rv = rng_func

    @property
    def parameters(self):
        return self.__parameters

    @property
    def size(self):
        try:
            return self.parameters['size']
        except KeyError:
            return 1, 1

    @size.setter
    def size(self, s):
        # Check for int entries
        assert all([isinstance(n, int) for n in s])
        self.__parameters['size'] = s

    def __mul__(self, other):
        if isinstance(other, RandomVariable):
            return RandomVariable(lambda: self.generate() * other.generate())
        elif isinstance(other, numbers.Number):
            return RandomVariable(lambda: self.generate() * other)
        else:
            raise Exception(f"Cannot multiply RandomVariable by {type(other)}")

    def __add__(self, other):
        if isinstance(other, RandomVariable):
            return RandomVariable(lambda: self.generate() + other.generate())
        elif isinstance(other, numbers.Number):
            return RandomVariable(lambda: self.generate() + other)
        else:
            raise Exception(f"Cannot add RandomVariable and {type(other)}")

    def __abs__(self):
        return RandomVariable(lambda: abs(self.generate()))

    def __pow__(self, power, modulo=None):
        if any(self.size>1) or any(power.size>1):
            raise Exception("Cannot use __pow__ method with vectors")
        if isinstance(power, RandomVariable):
            return RandomVariable(lambda: self.generate() ** power.generate())
        elif isinstance(power, numbers.Number):
            return RandomVariable(lambda: self.generate() ** power)
        else:
            raise Exception(f"Cannot elevate RandomVariable to {type(power)} power")

    def __sub__(self, other):
        if isinstance(other, RandomVariable):
            return RandomVariable(lambda: self.generate() - other.generate())
        elif isinstance(other, numbers.Number):
            return RandomVariable(lambda: self.generate() - other)
        else:
            raise Exception(f"Cannot subtract RandomVariable and {type(other)}")

    def __ceil__(self):
        return RandomVariable(lambda: math.ceil())

    # Generate numbers using the specified random variable
    def generate(self):
        return self.rv(**self.__parameters)

    # Change parameters to use the specified ones.
    def set_parameters(self, **rv_parameters):
        self.__parameters = rv_parameters


