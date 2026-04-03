import time

import hillclimber
import solution
import constants
import copy


class HILL_CLIMBER:
    def __init__(self):
        self.parent = solution.SOLUTION(self.nextAvailableID)
        self.nextAvailableID += 1

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.child.Evaluate("DIRECT")
        self.Select()
        self.Print()

    def Show_Best(self):
        self.parent.Evaluate("GUI")


    def Print(self):
        print("*************************************************************************************************")
        print("Parent's fitness: " + str(self.parent.fitness) + " Child's fitness: " + str(self.child.fitness))
        print("*************************************************************************************************")


    def Spawn(self):
        self.child = copy.deepcopy(self.parent)

    def Mutate(self):
        self.child.Mutate()

    def Select(self):
        if self.child.fitness < self.parent.fitness:
            # more neg = better
            self.parent = self.child

    def Evolve(self):
        self.parent.Evaluate("GUI")
        for currentGeneration in range(constants.numberOfGenerations):
            self.Evolve_For_One_Generation()
        