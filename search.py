import os
import hillclimber

hc = hillclimber.HILL_CLIMBER()
hc.Evolve()
hc.Show_Best()

'''for i in range(2):
    os.system("python generate.py")
    os.system("python simulate.py")'''