from time import time

import numpy as np
from pyrosim import pyrosim
import random
import os
import time
import constants as c
from pyrosim.material import MATERIAL
import pybullet as p



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
        self.Generate_Balls()

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

        x_off = c.ar_length/2 + (c.platform_thickness - c.side_wall_thickness) / 2
        z_off = 0.1 + c.ar_height + 1

        # Deltas from original torso position [0, 0, 1]
        dx = x_off - 0
        dz = z_off - 1

        pyrosim.Start_URDF("body.urdf")

        pyrosim.Send_Cube(name="Torso", pos=[x_off, 0, z_off], size=[length, width, height])

        # Joint positions shifted by dx/dz, cube pos values unchanged
        pyrosim.Send_Joint(name="Torso_BackLeg",  parent="Torso", child="BackLeg",  type="revolute", position=[dx+0,  -0.5, dz+1.0], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="BackLeg",  pos=[0,-0.5,0], size=[0.2,1,0.2])

        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[dx+0,   0.5, dz+1.0], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="FrontLeg", pos=[0,0.5,0], size=[0.2,1,0.2])

        pyrosim.Send_Joint(name="Torso_LeftLeg",  parent="Torso", child="LeftLeg",  type="revolute", position=[dx-0.5,  0,  dz+1.0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LeftLeg",  pos=[-0.5,0,0], size=[1,0.2,0.2])

        pyrosim.Send_Joint(name="Torso_RightLeg", parent="Torso", child="RightLeg", type="revolute", position=[dx+0.5,  0,  dz+1.0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="RightLeg", pos=[0.5,0,0], size=[1,0.2,0.2])

        pyrosim.Send_Joint(name="FrontLeg_FrontLowerLeg", parent="FrontLeg", child="FrontLowerLeg", type="revolute", position=[0, 1, 0], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0,0,-0.5], size=[0.2,0.2,1])

        pyrosim.Send_Joint(name="BackLeg_BackLowerLeg",   parent="BackLeg",  child="BackLowerLeg",  type="revolute", position=[0, -1, 0], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="BackLowerLeg",  pos=[0,0,-0.5], size=[0.2,0.2,1])

        pyrosim.Send_Joint(name="LeftLeg_LeftLowerLeg",   parent="LeftLeg",  child="LeftLowerLeg",  type="revolute", position=[-1, 0, 0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LeftLowerLeg",  pos=[0,0,-0.5], size=[0.2,0.2,1.0])

        pyrosim.Send_Joint(name="RightLeg_RightLowerLeg", parent="RightLeg", child="RightLowerLeg", type="revolute", position=[1, 0, 0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="RightLowerLeg", pos=[0,0,-0.5], size=[0.2,0.2,1.0])

        pyrosim.End()
        while not os.path.exists("body.urdf"):
            time.sleep(0.01)    

    def Generate_Balls(self):
        placed = []

        for i in range(300):
            radius = random.uniform(0.08, 0.5)

            # non-overlapping position
            for _ in range(100):
                x = random.uniform(-3, 3)
                y = random.uniform(-2, 2)
                if all(((x-px)**2 + (y-py)**2)**0.5 > radius + pr + 0.1 for px, py, pr in placed):
                    break

            body = p.createMultiBody(radius*50, p.createCollisionShape(p.GEOM_SPHERE, radius=radius),-1,[x, y, radius + i * 0.01])
            p.changeDynamics(body, -1, linearDamping=0.9, angularDamping=0.9, restitution=0.01)
            placed.append((x, y, radius))


    def Generate_Arena(self, length=c.ar_length, width=c.ar_width, height=c.ar_height,
                   side_wall_thickness=c.side_wall_thickness, platform_thickness=c.platform_thickness,
                   floor_thickness=c.floor_thickness):

        pyrosim.Start_URDF("arena.urdf")

        pyrosim.Send_Cube(
            name="Floor",
            pos=[0, 0, 0.1],
            size=[length, width, floor_thickness],

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
            #make arena hot pink

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
            #make arena hot pink

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
        

