#from simulation import SIMULATION
from motor import MOTOR
import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from pyrosim.neuralNetwork import NEURAL_NETWORK


class ROBOT:

    def __init__(self):
        self.robotId = p.loadURDF("body.urdf")
        self.nn = NEURAL_NETWORK("brain.nndf")

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
        for motor in self.motors:
            self.motors[motor].Set_Value(i)

    def Think(self):
        self.nn.Update()
        self.nn.Print()
            