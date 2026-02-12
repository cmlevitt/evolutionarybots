import numpy as np
import matplotlib.pyplot

#data_back = np.load("data/backLegSensorValues.npy")
#data_front = np.load("data/frontLegSensorValues.npy")
data_sin = np.load("data/SinusoidallyVaryingVals.npy")
#print(data)

#matplotlib.pyplot.plot(data_back, label="Back Leg", linewidth=3)
#matplotlib.pyplot.plot(data_front, label="Front Leg")
matplotlib.pyplot.plot(data_sin, label="Motor Comands")
matplotlib.pyplot.legend()
matplotlib.pyplot.show()