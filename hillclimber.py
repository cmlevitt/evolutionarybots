import hillclimber
import solution
import constants
import copy


class HILL_CLIMBER:
    def __init__(self):
        self.parent = solution.SOLUTION()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.child.Evaluate()
        self.Select()

    def Spawn(self):
        self.child = copy.deepcopy(self.parent)

    def Mutate(self):
        self.child.Mutate()

    def Select(self):
        pass

    def Evolve(self):
        self.parent.Evaluate()
        for currentGeneration in range(constants.numberOfGenerations):
            self.Evolve_For_One_Generation()
        