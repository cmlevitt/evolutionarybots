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
        self.amplitude = c.amplitude
        self.frequency = c.frequency
        self.offset = c.phaseOffset

        if self.jointName == b'Torso_BackLeg':
            self.frequency = c.frequency / 2

        self.motorValues = np.zeros(1000)

        for i in range (1000):
            self.motorValues[i] = self.amplitude * np.sin(self.frequency * 2*pi*i/1000 + self.offset)
        print(self.jointName, self.frequency)

    def Set_Value(self, i):
        pyrosim.Set_Motor_For_Joint(
                bodyIndex = self.robotId,
                jointName = self.jointName,
                controlMode = p.POSITION_CONTROL,
                targetPosition = self.motorValues[i], 
                maxForce = 100)
        
    def Save_Values(self):
        np.save("data/" + self.jointName + "MotorValues.npy", self.motorValues)
            