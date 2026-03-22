import hillclimber
import solution
import constants
import copy


class PARALELL_HILL_CLIMBER:
    def __init__(self):
        self.parents = {}
        for i in range(constants.populationSize):
            self.parents[i] = solution.SOLUTION()
        #print("parents dict: " + str(self.parents))

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.child.Evaluate("DIRECT")
        self.Select()
        self.Print()

    def Show_Best(self):
        #self.parent.Evaluate("GUI")
        pass

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
        for parent in self.parents:
            self.parents[parent].Evaluate("GUI")
        # self.parent.Evaluate("GUI")
        #for currentGeneration in range(constants.numberOfGenerations):
         #   self.Evolve_For_One_Generation()
        