from time import time

import numpy as np
from pyrosim import pyrosim
import random
import os
import time
import constants as c



class SOLUTION:
    def __init__(self, myID):
        self.myID = myID
        self.weights = np.random.random((c.numSensorNeurons, c.numMotorNeurons))
        self.weights = self.weights * 2 - 1

    def Set_ID(self, myID):
        self.myID = myID

    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Generate_Body()
        self.Generate_Brain()
        self.Generate_Arena()
        os.system("start /B python simulate.py " + directOrGUI + " " + str(self.myID))

    def Wait_For_Simulation_To_End(self):
        fitnessFileName = "fitness" + str(self.myID) + ".txt"
        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)

        while True:
            try:
                with open(fitnessFileName) as f:
                    self.fitness = float(f.read())
                break
            except (PermissionError, ValueError):
                time.sleep(0.01)

        os.system("del fitness" + str(self.myID) + ".txt")

    def Evaluate(self, directOrGUI):
        self.Create_World()
        self.Generate_Body()
        self.Generate_Brain()
        self.Generate_Arena()

        os.system("start /B python simulate.py " + directOrGUI + " " + str(self.myID))
        fitnessFileName = "fitness" + str(self.myID) + ".txt"
        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)

        with open(f"fitness{self.myID}.txt") as f:
            self.fitness = float(f.read())
        f.close()
        os.system("del fitness" + str(self.myID) + ".txt")

    def Mutate(self):
        randomRow = random.randint(0, c.numSensorNeurons - 1)
        randomColumn = random.randint(0, c.numMotorNeurons - 1)
        self.weights[randomRow][randomColumn] = random.random() * 2 - 1


    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.End()
        while not os.path.exists("world.sdf"):
            time.sleep(0.01)

    def Generate_Body(self):
        length = 1
        width = 1
        height = 1
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0,0,1] , size=[length, width, height])

        pyrosim.Send_Joint(name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [0,-0.5,1.0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLeg", pos=[0, -0.5, 0] , size=[0.2,1,0.2])

        pyrosim.Send_Joint(name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [0,0.5,1.0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLeg", pos=[0,0.5,0] , size=[0.2,1,0.2])

        pyrosim.Send_Joint(name = "Torso_LeftLeg" , parent= "Torso" , child = "LeftLeg" , type = "revolute", position = [-0.5,0,1.0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LeftLeg", pos=[-0.5,0,0] , size=[1,0.2,0.2])

        pyrosim.Send_Joint(name = "Torso_RightLeg" , parent= "Torso" , child = "RightLeg" , type = "revolute", position = [0.5,0,1.0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="RightLeg", pos=[0.5,0,0] , size=[1,0.2,0.2])

        pyrosim.Send_Joint(name = "FrontLeg_FrontLowerLeg" , parent= "FrontLeg" , child = "FrontLowerLeg" , type = "revolute", position = [0, 1, 0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0,0,-0.5] , size=[0.2,0.2,1])

        pyrosim.Send_Joint(name = "BackLeg_BackLowerLeg" , parent= "BackLeg" , child = "BackLowerLeg" , type = "revolute", position = [0, -1, 0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLowerLeg", pos=[0,0,-0.5] , size=[0.2,0.2,1])

        pyrosim.Send_Joint(name = "LeftLeg_LeftLowerLeg" , parent= "LeftLeg" , child = "LeftLowerLeg" , type = "revolute", position = [-1, 0, 0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0,0,-0.5] , size=[0.2,0.2,1.0])

        pyrosim.Send_Joint(name = "RightLeg_RightLowerLeg" , parent= "RightLeg" , child = "RightLowerLeg" , type = "revolute", position = [1, 0, 0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="RightLowerLeg", pos=[0,0,-0.5] , size=[0.2,0.2,1.0])

        pyrosim.End()
        while not os.path.exists("body.urdf"):
            time.sleep(0.01)

    def Generate_Arena(self, length=c.ar_length, width=c.ar_width, height=c.ar_height,
                   side_wall_thickness=c.side_wall_thickness, platform_thickness=c.platform_thickness,
                   floor_thickness=c.floor_thickness):

        pyrosim.Start_URDF("arena.urdf")

        # floor
        pyrosim.Send_Cube(
            name="Floor",
            pos=[0, 0, 0.1],
            size=[length, width, floor_thickness],
            #make arena pink
            color=[1, 0.75, 0.8]
        )

        # front wall
        pyrosim.Send_Joint(
            name="Floor_FrontWall",
            parent="Floor",
            child="FrontWall",
            type="fixed",
            position=[0, width/2, height/2]
        )
        pyrosim.Send_Cube(
            name="FrontWall",
            pos=[0, 0, 0],
            size=[length, side_wall_thickness, height],
            color=[1, 0.75, 0.8]
        )

        # back wall
        pyrosim.Send_Joint(
            name="Floor_BackWall",
            parent="Floor",
            child="BackWall",
            type="fixed",
            position=[0, -width/2, height/2]
        )
        pyrosim.Send_Cube(
            name="BackWall",
            pos=[0, 0, 0],
            size=[length, side_wall_thickness, height],
            color=[1, 0.75, 0.8]
        )

        #offset for makiing sure the walls are flush with floor and not intersecting it
        offset = (platform_thickness - side_wall_thickness) / 2

        #right wall
        pyrosim.Send_Joint(
            name="Floor_RightWall",
            parent="Floor",
            child="RightWall",
            type="fixed",
            position=[length/2 + offset, 0, height/2]
        )
        pyrosim.Send_Cube(
            name="RightWall",
            pos=[0, 0, 0],
            size=[platform_thickness, width, height],
            color=[1, 0.75, 0.8]
        )

        #lft wall
        pyrosim.Send_Joint(
            name="Floor_LeftWall",
            parent="Floor",
            child="LeftWall",
            type="fixed",
            position=[-length/2 - offset, 0, height/2]
        )
        pyrosim.Send_Cube(
            name="LeftWall",
            pos=[0, 0, 0],
            size=[platform_thickness, width, height],
            color=[1, 0.75, 0.8]
        )

        pyrosim.End()

        while not os.path.exists("arena.urdf"):
            time.sleep(0.01)


    def Generate_Brain(self): 
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        #pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        #pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
        #pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
        #pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "LeftLeg")
        #pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "RightLeg")

        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "BackLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "FrontLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "LeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 3, linkName = "RightLowerLeg")

        pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron( name = 5 , jointName = "Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron( name = 6 , jointName = "Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron( name = 7 , jointName = "Torso_RightLeg")

        pyrosim.Send_Motor_Neuron( name = 8 , jointName = "FrontLeg_FrontLowerLeg")
        pyrosim.Send_Motor_Neuron( name = 9 , jointName = "BackLeg_BackLowerLeg")
        pyrosim.Send_Motor_Neuron( name = 10 , jointName = "LeftLeg_LeftLowerLeg")
        pyrosim.Send_Motor_Neuron( name = 11 , jointName = "RightLeg_RightLowerLeg")

        #sensorNeurons = [0,1,2]
        #motorNeurons = [3,4]
        for currentRow in range(c.numSensorNeurons):
                for currentColumn in range(c.numMotorNeurons):
                    pyrosim.Send_Synapse( sourceNeuronName = currentRow, targetNeuronName = currentColumn + 3, weight = self.weights[currentRow][currentColumn] )

        pyrosim.End()
        while not os.path.exists(f"brain{self.myID}.nndf"):
            time.sleep(0.01)
        

