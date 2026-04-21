#from simulation import SIMULATION
import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import os

import solution

class WORLD:

    def __init__(self):
        while not os.path.exists("world.sdf"):
            time.sleep(0.01)
        self.planeId = p.loadURDF("plane.urdf")
        #make plane very dark gray
        p.changeVisualShape(self.planeId, -1, rgbaColor=[0.2, 0.2, 0.2, 1])
        # Load a sphere (position: x,y,z; orientation: quaternion)
        p.loadSDF("world.sdf")
        #spawn arena w fixed to the world
        self.arenaId = p.loadURDF("arena.urdf", useFixedBase=True)
        num_joints = p.getNumJoints(self.arenaId)
        for i in range(-1, num_joints):
            p.changeDynamics(self.arenaId, i,
                            restitution=0.0,
                            lateralFriction=1.0,
                            spinningFriction=1.0)
        #solution.SOLUTION.Generate_Balls(self)    

        
        #while not os.path.exists("world.sdf"):
        #    time.sleep(0.01)