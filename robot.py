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
        for linkName in ["Torso", "BackLowerLeg", "FrontLowerLeg", "LeftLowerLeg", "RightLowerLeg"]:
            self.sensors[linkName] = SENSOR(linkName)
        pass

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
                #print(neuronName, jointName, desiredAngle)

    def Think(self):
        self.nn.Update()
        #self.nn.Print()
    def Get_Fitness(self):

        state = p.getLinkState(self.robotId, 0)
        x = state[0][0]

        # --- COST TERMS (lower is better) ---

        forward_cost = -x            # more forward → LOWER cost
        movement_cost = -self.total_movement
        stall_cost = self.stall_steps

        # --- scaling ---
        forward_cost *= 5.0
        movement_cost *= 2.0
        stall_cost *= 0.3

        # --- total cost ---
        cost = forward_cost + movement_cost + stall_cost

        # optional clamp
        cost = max(cost, -5)

        with open("tmp" + str(self.myID) + ".txt", "w") as f:
            f.write(str(cost))

        os.replace("tmp"+str(self.myID)+".txt", "fitness"+str(self.myID)+".txt")

        os.system("del brain" + str(self.myID) + ".nndf")

    # def Get_Fitness(self):

    #     state = p.getLinkState(self.robotId, 0)
    #     x = state[0][0]

    #     # --- core objective: forward progress ---
    #     forward_progress = x

    #     # --- movement (normalized so it doesn't explode) ---
    #     movement = self.total_movement

    #     # --- stall measure (soft, not catastrophic penalty) ---
    #     stall = self.stall_steps

    #     # -----------------------------
    #     # SCALING (THIS IS THE KEY FIX)
    #     # -----------------------------

    #     # compress movement into usable range
    #     movement = movement / 10.0

    #     # compress stall so it doesn't dominate
    #     stall = stall / 100.0

    #     # -----------------------------
    #     # FITNESS COMPOSITION
    #     # -----------------------------

    #     fitness = (
    #         3.0 * forward_progress +
    #         1.5 * movement -
    #         0.5 * stall
    #     )

    #     # -----------------------------
    #     # SAFETY CLAMP (prevents collapse)
    #     # -----------------------------
    #     if fitness < -5:
    #         fitness = -5

    #     # -----------------------------
    #     # OUTPUT (your original format)
    #     # -----------------------------
    #     with open("tmp" + str(self.myID) + ".txt", "w") as f:
    #         f.write(str(fitness))

    #     os.replace("tmp"+str(self.myID)+".txt", "fitness"+str(self.myID)+".txt")

    #     os.system("del brain" + str(self.myID) + ".nndf")

    # def Get_Fitness(self): OG!
    #         stateOfLinkZero = p.getLinkState(self.robotId,0)
    #         positionOfLinkZero = stateOfLinkZero[0]
    #         xCoordinateOfLinkZero = positionOfLinkZero[0]
    #         with open("tmp" + str(self.myID) + ".txt", "w") as f:
    #             f.write(str(xCoordinateOfLinkZero))
    #         os.replace("tmp"+str(self.myID)+".txt" , "fitness"+str(self.myID)+".txt")

    #         os.system("del brain" + str(self.myID) + ".nndf")


        #print("Fitness check:", xCoordinateOfLinkZero)
    # def Get_Fitness(self):
    #     pos, _ = p.getBasePositionAndOrientation(self.robotId)
    #     x, y, z = pos[0], pos[1], pos[2]

    #     fitness = x  # reward crossing in -X direction

    #     # penalize leaving arena sideways
    #     arena_y = 2.0
    #     if abs(y) > arena_y:
    #         fitness += abs(y) * 2  # scale as needed

    #     # penalize falling over (root link too close to ground)
    #     if z < 0.1:
    #         fitness += 5.0

    #     with open("tmp" + str(self.myID) + ".txt", "w") as f:
    #         f.write(str(fitness))
    #     os.replace("tmp" + str(self.myID) + ".txt", "fitness" + str(self.myID) + ".txt")
    #     os.system("del brain" + str(self.myID) + ".nndf")