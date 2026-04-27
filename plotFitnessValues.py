import numpy as np
import matplotlib.pyplot as plt

MEDIUM = np.load("fitnessMedium2.npy") 
LOW = np.load("fitnessLow2.npy")  
HIGH = np.load("fitnessHigh2.npy")  


for i in range(HIGH.shape[0]):
    plt.plot(HIGH[i, :], linewidth=3.5, color="pink")
for i in range(MEDIUM.shape[0]):
    plt.plot(MEDIUM[i, :], linewidth=2.0, color="hotpink")
for i in range(LOW.shape[0]):
    plt.plot(LOW[i, :], linewidth=1.0, color="purple")
# for i in range(B.shape[0]):
#     plt.plot(B[i, :], linewidth=2.0, color="green")
# for i in range(C.shape[0]):
#     plt.plot(C[i, :], linewidth=3.5, color="red")

plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.title("Fitness by Friction Condition")
#plt.legend(["Low", "Medium", "High"])

plt.legend(labelcolor=["pink", "hotpink", "purple"], labels=["High", "Medium", "Low"])
plt.show()