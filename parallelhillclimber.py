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
    """
        self.child.Evaluate("DIRECT")
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
        id = 0
        for key in self.parents:
            child = str("child" + str(id))
            child = copy.deepcopy(self.parents[key])
            self.children[id] = child
            id += 1
        #self.child = copy.deepcopy(self.parent)
        #self.child.Set_ID(self.nextAvailableID)
        #self.nextAvailableID += 1
        #print("child's ID: " + str(self.child.myID))

    def Mutate(self):
        for child in self.children.values():
            child.Mutate()
            print("mutated")

    def Select(self):
        if self.child.fitness < self.parent.fitness:
            # more neg = better
            self.parent = self.child

    def Evolve(self):
        for parent in self.parents:
            self.parents[parent].Start_Simulation("DIRECT")
        for parent in self.parents:
            self.parents[parent].Wait_For_Simulation_To_End()
            #print("fitness: "+ str(self.parents[parent].fitness))
        # self.parent.Evaluate("GUI")
        for currentGeneration in range(constants.numberOfGenerations):
            self.Evolve_For_One_Generation()
        