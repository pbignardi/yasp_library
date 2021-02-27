import numpy as np
from typing import List


class Toolbox:
    # Check if number is a probability
    @staticmethod
    def is_probability(p: np.float64) -> bool:
        return True if 0 < p <= 1 else False

    # Check if list of floats is a probability density
    @staticmethod
    def is_density(p_list: List[np.float64]) -> bool:
        cumulative = sum(p_list)
        return True if 0.999 <= cumulative <= 1.0 else False

