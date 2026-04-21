import random

import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("world.sdf")
length = 1
width = 1
height = 1

#one link 
def Create_World():
    pyrosim.Start_SDF("world.sdf")
    Generate_Arena()
    #pyrosim.Send_Cube(name="Box", pos=[-5,3,0.5] , size=[length, width, height])
    pyrosim.End()

def Generate_Body():
    pyrosim.Start_URDF("body.urdf")
    pyrosim.Send_Cube(name="Torso", pos=[0,0,1.5] , size=[length, width, height])
    pyrosim.Send_Joint(name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [-0.5,0,1.0])
    pyrosim.Send_Cube(name="BackLeg", pos=[-0.5,0,-0.5] , size=[length, width, height])
    pyrosim.Send_Joint(name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [0.5,0,1.0])
    pyrosim.Send_Cube(name="FrontLeg", pos=[0.5,0,-0.5] , size=[length, width, height])
    pyrosim.End()

def Generate_Arena():
    pyrosim.Start_URDF("arena.urdf")
    pyrosim.Send_Cube(name="Ground", pos=[0,0,0.5] , size=[10, 10, 1], mass=0)
    pyrosim.End()

'''
def Create_Brain():
    pyrosim.Start_NeuralNetwork("brain.nndf")
    pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
    pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
    pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
    pyrosim.Send_Motor_Neuron( name = 3 , jointName = "Torso_BackLeg")
    pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_FrontLeg")
    #pyrosim.Send_Synapse( sourceNeuronName = 1 , targetNeuronName = 3 , weight = 1.0 )
    #pyrosim.Send_Synapse( sourceNeuronName = 2 , targetNeuronName = 3 , weight = -0.5 )
    #pyrosim.Send_Synapse( sourceNeuronName = 1 , targetNeuronName = 4 , weight = 2.0 )

    sensorNeurons = [0,1,2]
    motorNeurons = [3,4]
    for i in sensorNeurons:
        for j in motorNeurons:
            pyrosim.Send_Synapse( sourceNeuronName = i, targetNeuronName = j, weight = random.uniform(-1,1) )

    pyrosim.End()
'''
Create_World()
Generate_Body()
Generate_Arena()
#Create_Brain()