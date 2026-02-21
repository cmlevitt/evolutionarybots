from world import WORLD
from robot import ROBOT
import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim


class SIMULATION:

    def __init__(self):

        physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        #p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
        p.setGravity(0,0,-9.8,physicsClient)

        self.world = WORLD()
        self.robot = ROBOT()
        pyrosim.Prepare_To_Simulate(self.robot.robotId)
        self.robot.Prepare_To_Sense()
        self.robot.Prepare_To_Act(robotId=self.robot.robotId)
        

    def Run(self):
        for i in range(1000):
            time.sleep(1/60)
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Act(i)
            '''
            backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
            frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")

            pyrosim.Set_Motor_For_Joint(
                bodyIndex = self.robot.robotId,
                jointName = b'Torso_BackLeg',
                controlMode = p.POSITION_CONTROL,
                targetPosition = targetAngles_bk[i], 
                maxForce = 100)

            pyrosim.Set_Motor_For_Joint(
                bodyIndex = self.robot.robotId,
                jointName = b'Torso_FrontLeg',
                controlMode = p.POSITION_CONTROL,
                targetPosition = targetAngles_fr[i],
                maxForce = 100)
                '''
            #print(i)

    def __del__(self): #destructor
        p.disconnect()
            
                ##step 27