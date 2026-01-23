import pybullet as p
import time
physicsClient = p.connect(p.GUI)
p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
#physicsClient = p.connect(p.GUI)
p.loadSDF("box.sdf")
for i in range(1000):
    time.sleep(1/60)
    p.stepSimulation()
    print(i)
p.disconnect()