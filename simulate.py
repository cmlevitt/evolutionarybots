import random as random
import pybullet as p
from simulation import SIMULATION
import sys


directOrGUI = sys.argv[1]
solutionID = sys.argv[2]
simulation = SIMULATION(directOrGUI, solutionID)

simulation.Run()
simulation.Get_Fitness()
p.disconnect()

