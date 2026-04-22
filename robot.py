#from simulation import SIMULATION
from motor import MOTOR
import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import constants as c
import numpy as np

class ROBOT:

    def __init__(self, solutionID):
        self.total_movement = 0
        self.stall_steps = 0
        self.prev_x = None
        self.robotId = p.loadURDF("body.urdf")
        while not os.path.exists("body.urdf"):
            time.sleep(0.02)
        
        for cube in range(p.getNumJoints(self.robotId)):
            p.changeVisualShape(self.robotId, cube, rgbaColor=[0.9, 0.75, 0.8, 1])
        p.changeVisualShape(self.robotId, -1, rgbaColor=[0.9, 0.75, 0.8, 1])
        while not os.path.exists("body.urdf"):
            time.sleep(0.01)
        self.myID = solutionID
        self.nn = NEURAL_NETWORK("brain" + str(self.myID) + ".nndf")
    

    def Prepare_To_Sense(self):
        self.sensors = {}
        # for linkname in ["BackLowerLeg", "FrontLowerLeg", "LeftLowerLeg", "RightLowerLeg"]:
        for linkName in ["BackLeg", "FrontLeg", "LeftLeg", "RightLeg",
                        "BackLowerLeg", "FrontLowerLeg", "LeftLowerLeg", "RightLowerLeg"]:
            self.sensors[linkName] = SENSOR(linkName)

    def Sense(self, i):
        for sensor in self.sensors:
            self.sensors[sensor].Get_Value(i)
            # if i == 100:
            #     for sensor in self.sensors:
            #         print(sensor, self.sensors[sensor].values[100])

    def Prepare_To_Act(self, robotId):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName, self.robotId)
    

    def Act(self, i):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = (self.nn.Get_Value_Of(neuronName)* c.motorJointRange)
                self.motors[jointName.encode()].Set_Value(self.robotId, desiredAngle)
        # for idx, jointName in enumerate(pyrosim.jointNamesToIndices):
        #     # set angle
        #     angle = c.motorJointRange * np.sin(i * 0.1 + idx * 0.5)
        #     try:
        #         self.motors[jointName].Set_Value(self.robotId, angle)
        #     except KeyError:
        #         self.motors[jointName.encode()].Set_Value(self.robotId, angle)
        #     if i % 100 == 0:
        #         print(f"Step {i}: joint {jointName}, angle {angle:.3f}")
                # #print(neuronName, jointName, desiredAngle)

    def Think(self):
        self.nn.Update()
        #self.nn.Print()
   
    def Get_Fitness(self):

        # stateOfLinkZero = p.getLinkState(self.robotId, 0)
        # positionOfLinkZero = stateOfLinkZero[0]
        # xCoordinateOfLinkZero = positionOfLinkZero[0]
        pos, _ = p.getBasePositionAndOrientation(self.robotId)
        #x = pos[0]
        x, y, z = pos

        stall_penalty = 0.001 * self.stall_steps

        # penalize falling over
        fall_penalty = 10.0 if z < 1.2 else 0.0

        displacement = 2.0 - x  # positive when moving in -x from spawn at 2.0
        fitness = -displacement + stall_penalty + fall_penalty  # minimize displacement and stall, heavily penalize falling over

        #fitness = xCoordinateOfLinkZero + stall_penalty
        fell = z < 1.2

        #trying to debug fitness values, log to file
        with open("fitness_log.txt", "a") as log:
            log.write(f"[{self.myID}] x={x:.2f} z={z:.2f} fell={fell} stall={self.stall_steps}\n")
        with open("tmp" + str(self.myID) + ".txt", "w") as f:
            f.write(str(fitness))

        os.replace("tmp"+str(self.myID)+".txt", "fitness"+str(self.myID)+".txt")

        os.system("del brain" + str(self.myID) + ".nndf")


    # def Get_Fitness(self): OG!
    #         stateOfLinkZero = p.getLinkState(self.robotId,0)
    #         positionOfLinkZero = stateOfLinkZero[0]
    #         xCoordinateOfLinkZero = positionOfLinkZero[0]
    #         with open("tmp" + str(self.myID) + ".txt", "w") as f:
    #             f.write(str(xCoordinateOfLinkZero))
    #         os.replace("tmp"+str(self.myID)+".txt" , "fitness"+str(self.myID)+".txt")

    #         os.system("del brain" + str(self.myID) + ".nndf")


