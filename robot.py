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

class ROBOT:

    def __init__(self, solutionID):
        self.robotId = p.loadURDF("body.urdf")
        
        for cube in range(p.getNumJoints(self.robotId)):
            p.changeVisualShape(self.robotId, cube, rgbaColor=[0.9, 0.75, 0.8, 1])
        p.changeVisualShape(self.robotId, -1, rgbaColor=[0.9, 0.75, 0.8, 1])
        while not os.path.exists("body.urdf"):
            time.sleep(0.01)
        self.myID = solutionID
        self.nn = NEURAL_NETWORK("brain" + str(self.myID) + ".nndf")
    

    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)
        pass

    def Sense(self, i):
        for sensor in self.sensors:
            self.sensors[sensor].Get_Value(i)

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
                #print(neuronName, jointName, desiredAngle)

    def Think(self):
        self.nn.Update()
        #self.nn.Print()
            
    def Get_Fitness(self):
        stateOfLinkZero = p.getLinkState(self.robotId,0)
        positionOfLinkZero = stateOfLinkZero[0]
        xCoordinateOfLinkZero = positionOfLinkZero[0]
        with open("tmp" + str(self.myID) + ".txt", "w") as f:
            f.write(str(xCoordinateOfLinkZero))
        os.replace("tmp"+str(self.myID)+".txt" , "fitness"+str(self.myID)+".txt")

        os.system("del brain" + str(self.myID) + ".nndf")
        #print("Fitness check:", xCoordinateOfLinkZero)