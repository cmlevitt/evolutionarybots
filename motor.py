from pyrosim import pyrosim, robot
import pybullet as p
import constants as c
import numpy as np
from math import pi

class MOTOR:

    def __init__(self, jointName, robotId):
        self.jointName = jointName
        self.robotId = robotId
        self.motorValues = np.zeros(1000)
        self.Prepare_To_Act()
    
    def Prepare_To_Act(self):
        self.amplitude = c.amplitude_bk
        self.frequency = c.frequency_bk
        self.offset = c.phaseOffset_bk
        
        targetAngles_bk = np.zeros(1000)
        for i in range (1000):
            targetAngles_bk[i] = self.amplitude * np.sin(self.frequency * 2*pi*i/1000 + self.offset)

        targetAngles_fr = np.zeros(1000)
        for i in range (1000):
            targetAngles_fr[i] = self.amplitude * np.sin(self.frequency * 2*pi*i/1000 + self.offset)

    def Set_Value(self, i):
        pyrosim.Set_Motor_For_Joint(
                bodyIndex = self.robotId,
                jointName = self.jointName,
                controlMode = p.POSITION_CONTROL,
                targetPosition = self.motorValues[i], 
                maxForce = 100)
            