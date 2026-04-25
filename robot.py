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

    def Think(self):
        self.nn.Update()
        #self.nn.Print()
   
    def Get_Fitness(self):

        pos, _ = p.getBasePositionAndOrientation(self.robotId)
        #x = pos[0]
        x, y, z = pos

        #penalize movement in pos x direction past spawn point
        backwards_penalty = 0.0
        if x > c.ar_length / 2 - 2.0:
            backwards_penalty = 5.0 * (x - (c.ar_length / 2 - 2.0))  # penalize more the further past spawn point


        stall_penalty = 0.001 * self.stall_steps

        # penalize falling over
        
        fall_penalty = 0.0
        jump_penalty = 0.0

        if self.min_z < 1.2: # sunk or out of arena
            fall_penalty = 50.0
        elif self.min_z < 1.8: # sinking or barely standing
            fall_penalty = 10.0
        elif self.max_z > 5.0: # big jump
            jump_penalty = 50.0
        elif self.max_z > 3.5: #smaller jumping
            jump_penalty = 10.0

        spawn_x = c.ar_length / 2 - 2.0
        displacement = spawn_x - x  # positive when moving in -x from spawn 

        fitness = -displacement + backwards_penalty + stall_penalty + jump_penalty + fall_penalty  # fitness = distance traveled in -x direction minus penalties

        #fitness = xCoordinateOfLinkZero + stall_penalty
        fell = self.min_z < 1.8
        jumped = self.max_z > 3.5

        #trying to debug fitness values, log to file
        with open("fitness_log.txt", "a") as log:
            log.write(f"[{self.myID}] fitness={fitness:.2f} x={x:.2f} min_z={self.min_z:.2f} max_z={self.max_z:.2f} fell={fell} jumped={jumped} stall={self.stall_steps}\n")
        with open("tmp" + str(self.myID) + ".txt", "w") as f:
            f.write(str(fitness))

        os.replace("tmp"+str(self.myID)+".txt", "fitness"+str(self.myID)+".txt")

        os.system("del brain" + str(self.myID) + ".nndf")



