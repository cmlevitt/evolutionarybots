import numpy as np
from pyrosim import pyrosim

class SENSOR:
    def __init__(self, linkName):
        self.linkName = linkName
        self.values = np.zeros(1000)
        all_links = ["BackLeg", "FrontLeg", "LeftLeg", "RightLeg",
                    "BackLowerLeg", "FrontLowerLeg", "LeftLowerLeg", "RightLowerLeg"]
        idx = all_links.index(linkName) if linkName in all_links else 0
        self.phase = idx * (np.pi / 4)

    def Get_Value(self, i):
        self.values[i % 1000] = np.sin(i * 0.1 + self.phase)


    def Save_Values(self):
        np.save("data/" + self.linkName + "SensorValues.npy", self.values)

