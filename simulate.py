from math import pi
import random as random
import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import numpy as np

amplitude_bk = pi/4
frequency_bk = 10
phaseOffset_bk = 0

amplitude_fr = pi/4
frequency_fr = 10
phaseOffset_fr = -0.5

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)

p.setGravity(0,0,-9.8,physicsClient)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")

#p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robotId)
backLegSensorValues = np.zeros(1000)
frontLegSensorValues = np.zeros(1000)

#values = np.linspace(0, 2*pi, 1000)
'''
targetAngles = np.sin(values)
targetAngles = targetAngles * (pi/4) 
'''
targetAngles_bk = np.zeros(1000)
for i in range (1000):
    targetAngles_bk[i] = amplitude_bk * np.sin(frequency_bk * 2*pi*i/1000 + phaseOffset_bk)

targetAngles_fr = np.zeros(1000)
for i in range (1000):
    targetAngles_fr[i] = amplitude_fr * np.sin(frequency_fr * 2*pi*i/1000 + phaseOffset_fr)
'''
np.save("data/SinusoidallyVaryingVals.npy", targetAngles)
exit() '''

for i in range(1000):
    time.sleep(1/60)
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")

    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = b'Torso_BackLeg',
        controlMode = p.POSITION_CONTROL,
        targetPosition = targetAngles_bk[i], 
        maxForce = 100)

    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = b'Torso_FrontLeg',
        controlMode = p.POSITION_CONTROL,
        targetPosition = targetAngles_fr[i],
        maxForce = 100)
        #print(i)

#print(backLegSensorValues)
#np.save("data/backLegSensorValues.npy", backLegSensorValues)
#np.save("data/frontLegSensorValues.npy", frontLegSensorValues)
np.save("data/SinusoidallyVaryingValsFront.npy", targetAngles_fr)
np.save("data/SinusoidallyVaryingValsBack.npy", targetAngles_bk)
p.disconnect()