import numpy as np
import matplotlib.pyplot

data_back = np.load("data/backLegSensorValues.npy")
data_front = np.load("data/frontLegSensorValues.npy")
#print(data)

matplotlib.pyplot.plot(data_back, label="Back Leg", linewidth=3)
matplotlib.pyplot.plot(data_front, label="Front Leg")
matplotlib.pyplot.legend()
matplotlib.pyplot.show()