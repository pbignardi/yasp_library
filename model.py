from pyomo.environ import AbstractModel, Var, Suffix, Param
from typing import List


class AbstractSubproblem(AbstractModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__random_variables: list = []
        self.dual = Suffix(direction=Suffix.IMPORT)
        self.rc = Suffix(direction=Suffix.IMPORT)

    @property
    def variables(self):
        return self.component_data_objects(Var)

    @property
    def get_state_variables(self):
        return [v for v in self.variables if hasattr(v, 'is_state') and v.is_state]


# This function takes the place of a class StateVar, it builds a Var and set the var 'is_state' as true.
def make_state_var(*args, **kwargs):
    v = Var(*args, **kwargs)
    setattr(v, 'is_state', True)
    return v



