import random as random
import pybullet as p
from simulation import SIMULATION

simulation = SIMULATION()
simulation.Run()
p.disconnect()
