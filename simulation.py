
from world import WORLD
from robot import ROBOT
import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import random as random
import constants as c


class SIMULATION:

    def __init__(self, directOrGUI, solutionID):
        self.directOrGUI = directOrGUI
        self.solutionID = solutionID
        if directOrGUI == "GUI":
            physicsClient = p.connect(p.GUI, options="--background_color_red=1 --background_color_green=.957 --background_color_blue=0.992")
            #time.sleep(1/60) didnt fix
        else:
            physicsClient = p.connect(p.DIRECT)
        p.resetSimulation()
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        #p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
        p.setGravity(0,0,-9.8,physicsClient)

        self.world = WORLD()
        self.Generate_Balls()
        self.robot = ROBOT(self.solutionID)
        pyrosim.Prepare_To_Simulate(self.robot.robotId)
        self.robot.Prepare_To_Sense()
        self.robot.Prepare_To_Act(robotId=self.robot.robotId)

    def Generate_Balls(self):
        # generate balls in a grid pattern with some random offset,  avoid spawning them too close to the robot's starting position
        spacing = 0.28
        cols, rows = 26, 17

        # center the grid around the origin
        x_start = -((cols - 1) * spacing) / 2  
        y_start = -((rows - 1) * spacing) / 2

        # spawn balls with random offsets
        for i in range(cols * rows):
            x = x_start + (i % cols) * spacing + random.uniform(-0.05, 0.05)
            y = y_start + (i // cols) * spacing + random.uniform(-0.05, 0.05)
            spawn_x = c.ar_length / 2 - 1.0
            # avoid spawning balls too close to the robot's starting position (within 0.8 units)
            if (x - spawn_x)**2 + y**2 < 0.64:
                continue
            # randomize ball size and physics properties
            r = random.uniform(0.12, 0.35)
            # make larger balls heavier 
            col = p.createCollisionShape(p.GEOM_SPHERE, radius=r)
            body = p.createMultiBody(r * 200, col, -1, [x, y, random.uniform(0.3, 1.5)])
            p.changeDynamics(body, -1,
                lateralFriction=0.1,
                rollingFriction=0.1,
                spinningFriction=0.1,
                restitution=0.0,
                linearDamping=0.1,    
                angularDamping=0.1)
                
            if i % 30 == 0:
                for _ in range(10):
                    p.stepSimulation()

        for _ in range(50):
            p.stepSimulation()

    def Run(self):
        import time
        
        t0 = time.time()
        # for i in range(500):
        #     p.stepSimulation()
        #print(f"Ball-drop phase: {time.time()-t0:.3f}s")

        t1 = time.time()
        # reset movement tracking variables before the robot starts moving
        self.robot.total_movement = 0
        self.robot.stall_steps = 0
        self.robot.prev_x = None

        # run the main simulation loop, track movement and apply stall penalty
        for i in range(1000):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)

            state = p.getLinkState(self.robot.robotId, 0)
            x = state[0][0]

            # track total movement and stall steps for fitness penalty
            if self.robot.prev_x is None:
                self.robot.prev_x = x
            else:
                # calculate movement since last step
                dx = abs(x - self.robot.prev_x)

                # add to total movement
                self.robot.total_movement += dx

                # add stall penalty if movement is very small
                if dx < 0.0005:
                    self.robot.stall_steps += 1

                # reset stall penalty if movement is large
                self.robot.prev_x = x

            if self.directOrGUI == "GUI":
                time.sleep(1/60) #TIME DELAY

    # def Run(self):
    #     for i in range(500): #let balls fall before starting to move
    #         p.stepSimulation()
    #     for i in range(2000):
    #         p.stepSimulation()

    #         self.robot.Sense(i)
    #         self.robot.Think()
    #         self.robot.Act(i)

    #     #if self.directOrGUI == "GUI":
    #         #time.sleep(1/60) #TIME DELAY
        

    def Get_Fitness(self):
        self.robot.Get_Fitness()
        

    def __del__(self): #destructor
        p.disconnect()
        