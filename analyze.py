import numpy as np
import matplotlib.pyplot

#data_back = np.load("data/backLegSensorValues.npy")
#data_front = np.load("data/frontLegSensorValues.npy")
#data_sin = np.load("data/SinusoidallyVaryingVals.npy")
data_sin_front = np.load("data/SinusoidallyVaryingValsFront.npy")
data_sin_back = np.load("data/SinusoidallyVaryingValsBack.npy")
#print(data)

matplotlib.pyplot.plot(data_sin_back, label="Back Leg", linewidth=3)
matplotlib.pyplot.plot(data_sin_front, label="Front Leg")#matplotlib.pyplot.plot(data_sin, label="Motor Comands")
matplotlib.pyplot.legend()
matplotlib.pyplot.show()