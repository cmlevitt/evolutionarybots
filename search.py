import os
import time
import parallelhillclimber
import parallelhillclimber
import random
import numpy as np

#results vary way too much bc of ball placement, so set seeds for reproducibility
# random.seed(42)
# np.random.seed(42)
random.seed(42)
np.random.seed(42)

#close debug log to clear
open("fitness_log.txt", "w").close()
phc = parallelhillclimber.PARALELL_HILL_CLIMBER()
phc.Evolve()
#time.sleep(1/60) 
phc.Show_Best()

'''for i in range(2):
    os.system("python generate.py")
    os.system("python simulate.py")'''