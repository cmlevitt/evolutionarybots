import numpy as np
from pyrosim import pyrosim

class SENSOR:

    def __init__(self, linkName):

        self.linkName = linkName
        self.values = np.zeros(1000)

        #print(self.values)

    def Get_Value(self, i):
        #if i == 999:
            #print(self.values[i])
            pass

    def Save_Values(self):
        np.save("data/" + self.linkName + "SensorValues.npy", self.values)

