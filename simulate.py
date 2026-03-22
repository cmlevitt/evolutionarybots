import random as random
import pybullet as p
from simulation import SIMULATION
import sys


directOrGUI = sys.argv[1]
simulation = SIMULATION(directOrGUI)

simulation.Run()
simulation.Get_Fitness()
p.disconnect()

