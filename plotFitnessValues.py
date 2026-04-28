import numpy as np
import matplotlib.pyplot as plt

MEDIUM1 = np.load("finalFit_medium01.npy") 
MEDIUM2 = np.load("finalFit_medium02.npy")
MEDIUM3 = np.load("finalFit_medium03.npy")  
MEDIUM4 = np.load("finalFit_medium04.npy")
MEDIUM5 = np.load("finalFit_medium05.npy")


LOW1 = np.load("finalFit_low01.npy")  
LOW2 = np.load("finalFit_low02.npy")
LOW3 = np.load("finalFit_low03.npy")
LOW4 = np.load("finalFit_low04.npy")
LOW5 = np.load("finalFit_low05.npy")


HIGH1 = np.load("finalFit_high01.npy") 
HIGH2 = np.load("finalFit_high02.npy")
HIGH3 = np.load("finalFit_high03.npy")
HIGH4 = np.load("finalFit_high04.npy")
HIGH5 = np.load("finalFit_high05.npy")

#take fitness averages across runs for each friction condition
# high_avg = np.mean(HIGH, axis=0)
# medium_avg = np.mean(MEDIUM, axis=0)
# low_avg = np.mean(LOW, axis=0)

# Plot fitness averages for each friction condition

# plt.plot(high_avg, linewidth=3.5, color="pink", label="High")
# plt.plot(medium_avg, linewidth=2.5, color="hotpink", label="Medium")
# plt.plot(low_avg, linewidth=2.0, color="purple", label="Low")


#plot all fitness values for each friction condition

for i in range(HIGH1.shape[0]):
    plt.plot(HIGH1[i, :], linewidth=3.5, color="pink")
for i in range(HIGH2.shape[0]):
    plt.plot(HIGH2[i, :], linewidth=3.5, color="pink")
for i in range(HIGH3.shape[0]):
    plt.plot(HIGH3[i, :], linewidth=3.5, color="pink")
for i in range(HIGH4.shape[0]):
    plt.plot(HIGH4[i, :], linewidth=3.5, color="pink")
for i in range(HIGH5.shape[0]):
    plt.plot(HIGH5[i, :], linewidth=3.5, color="pink")

for i in range(MEDIUM1.shape[0]):
    plt.plot(MEDIUM1[i, :], linewidth=2.0, color="hotpink")
for i in range(MEDIUM2.shape[0]):
    plt.plot(MEDIUM2[i, :], linewidth=2.0, color="hotpink")
for i in range(MEDIUM3.shape[0]):
    plt.plot(MEDIUM3[i, :], linewidth=2.0, color="hotpink")
for i in range(MEDIUM4.shape[0]):
    plt.plot(MEDIUM4[i, :], linewidth=2.0, color="hotpink")
for i in range(MEDIUM5.shape[0]):
    plt.plot(MEDIUM5[i, :], linewidth=2.0, color="hotpink")

for i in range(LOW1.shape[0]):
    plt.plot(LOW1[i, :], linewidth=1.0, color="purple")
for i in range(LOW2.shape[0]):
    plt.plot(LOW2[i, :], linewidth=1.0, color="purple")
for i in range(LOW3.shape[0]):
    plt.plot(LOW3[i, :], linewidth=1.0, color="purple")
for i in range(LOW4.shape[0]):
    plt.plot(LOW4[i, :], linewidth=1.0, color="purple")
for i in range(LOW5.shape[0]):
    plt.plot(LOW5[i, :], linewidth=1.0, color="purple")


plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.title("Fitness by Friction Condition - Averages")
#plt.legend(["Low", "Medium", "High"])

plt.legend(labelcolor=["pink", "hotpink", "purple"], labels=["High", "Medium", "Low"])
plt.show()