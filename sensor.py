import numpy as np
from pyrosim import pyrosim

class SENSOR:

    def __init__(self, linkName):

        self.linkName = linkName
        self.values = np.zeros(1000)

        #print(self.values)

    def Get_Value(self, i):
        self.values[i] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
    #print only last time step value
        if i == 999:
            print(self.values[i])
