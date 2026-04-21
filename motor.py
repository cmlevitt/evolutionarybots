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

    def Set_Value(self, robot, desiredAngle):
        pyrosim.Set_Motor_For_Joint(
                bodyIndex = self.robotId,
                jointName = self.jointName,
                controlMode = p.POSITION_CONTROL,
                targetPosition = desiredAngle, 
                maxForce = 300)
    