import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf")
length = 1
width = 1
height = 1
x= 0
y=0
z=0.5

#5 rows 5 cols
for j in range (5):
    for k in range (5):
        length =1
        width=1
        height=1
        for i in range(10):
            pyrosim.Send_Cube(name="Box", pos=[x,y,z] , size=[length, width, height])
            z=z+1
            length=length*.9
            width=width*.9
            height=height*.9
        pyrosim.Send_Cube(name="Box", pos=[x,y,z] , size=[length, width, height])
        x=x+1.5
    y=y+1.5
    x=0
    z=0.5


pyrosim.End()

