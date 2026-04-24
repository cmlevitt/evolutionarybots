from random import seed
from time import time

import hillclimber
import solution
import constants
import copy
import os
import constants as c

class PARALELL_HILL_CLIMBER:
    def __init__(self):
        os.system("del brain*" + ".nndf")
        os.system("del fitness*" + ".txt")
        self.Generate_Ball_Config() 
        self.parents = {}
        self.nextAvailableID = 0
        for i in range(constants.populationSize):
            self.parents[i] = solution.SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
        #print("parents dict: " + str(self.parents))

    def Generate_Ball_Config(self):
        import json
        import random
        import time
        seed = int(time.time())
        random.seed(seed)
        print(f"Ball seed: {seed}")  # save to reproduce the same ball configuration (if good)
        spacing = 0.28
        cols, rows = 38, 17
        x_start = -((cols - 1) * spacing) / 2
        y_start = -((rows - 1) * spacing) / 2
        spawn_x = c.ar_length / 2 - 2.0
        balls = []
        for i in range(cols * rows):
            x = x_start + (i % cols) * spacing + random.uniform(-0.05, 0.05)
            y = y_start + (i // cols) * spacing + random.uniform(-0.05, 0.05)
            if (x - spawn_x)**2 + y**2 < 0.64:
                continue
            r = random.uniform(0.12, 0.35)
            z = random.uniform(0.3, 1.5)
            balls.append({"x": x, "y": y, "z": z, "r": r})
        with open("balls.json", "w") as f:
            json.dump(balls, f)
        random.seed()# reset random seed to system time for evolution

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()

    def Show_Best(self):
        #self.parents.Evaluate("GUI")
        bestParent = None
        mostFit = None
        for key in self.parents:
            if mostFit == None or self.parents[key].fitness < mostFit:
                mostFit = self.parents[key].fitness
                bestParent = key
        #directOrGUI = "GUI"
        self.parents[bestParent].Start_Simulation("GUI")
        #time.sleep(1/100) 
        
        self.parents[bestParent].Wait_For_Simulation_To_End()


    def Print(self):
        for key in self.parents:
            print("*************************************************************************************************")
            print("Parent " + str(key) + ": " + str(self.parents[key].fitness) + " Child's fitness: " + str(self.children[key].fitness))

    def Spawn(self):
        self.children = {}
        for id, key in enumerate(self.parents):
            self.children[key] = copy.deepcopy(self.parents[key])
        #self.child = copy.deepcopy(self.parent)
            self.children[key].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1
        #print("child's ID: " + str(self.child.myID))

    def Mutate(self):
        for child in self.children.values():
            child.Mutate()

    def Select(self):
        for key in self.parents:
            if self.children[key].fitness < self.parents[key].fitness:
                # more neg = better
                self.parents[key] = self.children[key]

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

