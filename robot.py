#from simulation import SIMULATION
import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR

class ROBOT:

    def __init__(self):

        self.sensors = {}
        self.motors = {}
        self.robotId = p.loadURDF("body.urdf")

    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)
        pass

    def Sense(self, i):
        for sensor in self.sensors:
            self.sensors[sensor].Get_Value(i)