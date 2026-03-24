import hillclimber
import solution
import constants
import copy
import os

class PARALELL_HILL_CLIMBER:
    def __init__(self):
        os.system("del brain*" + ".nndf")
        os.system("del fitness*" + ".txt")
        self.parents = {}
        self.nextAvailableID = 0
        for i in range(constants.populationSize):
            self.parents[i] = solution.SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
        #print("parents dict: " + str(self.parents))

    def Evolve_For_One_Generation(self):


        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        exit()
    """
        self.Select()
        self.Print()
"""
    def Show_Best(self):
        #self.parent.Evaluate("GUI")
        pass

    def Print(self):
        print("*************************************************************************************************")
        print("Parent's fitness: " + str(self.parent.fitness) + " Child's fitness: " + str(self.child.fitness))
        print("*************************************************************************************************")


    def Spawn(self):
        self.children = {}
        for id, key in enumerate(self.parents):
            childkey = "child" + str(id)
            self.children[childkey] = copy.deepcopy(self.parents[key])
        #self.child = copy.deepcopy(self.parent)
        #self.child.Set_ID(self.nextAvailableID)
        #self.nextAvailableID += 1
        #print("child's ID: " + str(self.child.myID))

    def Mutate(self):
        for child in self.children.values():
            child.Mutate()

    def Select(self):
        if self.child.fitness < self.parent.fitness:
            # more neg = better
            self.parent = self.child

    def Evaluate(self, solutions):
        for parent in solutions:
            solutions[parent].Start_Simulation("DIRECT")
        for parent in solutions:
            solutions[parent].Wait_For_Simulation_To_End()

    def Evolve(self):
        self.Evaluate(self.parents)
        #exit()
        
            #print("fitness: "+ str(self.parents[parent].fitness))
        # self.parent.Evaluate("GUI")
        for currentGeneration in range(constants.numberOfGenerations):
            self.Evolve_For_One_Generation()

