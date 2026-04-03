import os
import time
import parallelhillclimber
import parallelhillclimber

phc = parallelhillclimber.PARALELL_HILL_CLIMBER()
phc.Evolve()
#time.sleep(1/60) didnt fix
phc.Show_Best()

'''for i in range(2):
    os.system("python generate.py")
    os.system("python simulate.py")'''