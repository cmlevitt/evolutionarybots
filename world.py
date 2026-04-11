#from simulation import SIMULATION
import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import os

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

        # Create a sphere
        sphereRadius = 0.5
        colSphereId = p.createCollisionShape(p.GEOM_SPHERE, radius=sphereRadius)
        visualShapeId = -1 
        self.sphereId = p.createMultiBody(1, colSphereId, -1, [0, 0, 2]) # Mass 1, Position 2m high
        #loop 30 spheres ranging in size from .2 to 1 to fill the arena
        #vary where they are in the arena as well
        for i in range(30):
            radius = 0.2 + 0.3 * (i / 29)  # Vary radius from 0.2 to 0.5
            colSphereId = p.createCollisionShape(p.GEOM_SPHERE, radius=radius)
            visualShapeId = -1 
            x = -5 + 10 * (i / 29)  # vary from -5 to 5 across the arena
            y = -2 + 4 * (i / 29)  # 
            z = radius  
            p.createMultiBody(4, colSphereId, visualShapeId, [x, y, z]) # Mass 1, Position
        
        #while not os.path.exists("world.sdf"):
        #    time.sleep(0.01)