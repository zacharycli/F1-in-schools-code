import math
from matplotlib import pyplot as plt
def getpoint(center, diameter, rotation):
    rot = math.pi*2*-rotation
    return [center[0]+math.cos(rot)*diameter/2, center[0]+math.sin(rot)*diameter/2]
def getspeed(rotation,speed,d):
    rot = math.pi*2*rotation
    return [math.sin(rot)*speed*(d/diam)+speed, math.cos(rot)*speed*(d/diam)]
def mag(vector):
    total= 0
    for i in vector:
        total += i**2
    return math.sqrt(total)
x = []
miny = []
maxy =[]
y= []
#wheel sim
for q in range(6):
    speed = 10
    diam = 0.026
    rps = speed/(math.pi*diam)
    t = 0
    r=0
    ma = 0
    mi = 10**9
    sims = 5
    points = 80000
    layers = 200
    totalmass = 0.05
    chassismass = q/100
    energy = 0
    for a in range(sims):
        particles = [[[0,diam/2],[speed,0],chassismass]]
        #each particle [[x,y],[xvel,yvel],mass]
        #car body is one particle. wheel particles have same mass as each other.
        for j in range(layers):
            for i in range(int(points/layers)):
                particles.append([getpoint(particles[0][0], diam*((j+1)/layers), ((i+1)/(points/layers))+r),getspeed(((i+1)/(points/layers))+r,speed,diam*((j+1)/layers)),(totalmass-chassismass)/points])
        
        t+=1
        r = t*rps
        denergy = 0
        total_speed = [0,0]
        for i in particles:
            denergy += mag(i[1])**2*i[2]*0.5
            total_speed[0] += i[1][0]/len(particles)
            total_speed[1] += i[1][1]/len(particles)
        energy += denergy
        if denergy > ma:
            ma = denergy
        if denergy < mi:
            mi = denergy
    x.append((totalmass-chassismass)*100/totalmass)
    miny.append(mi)
    maxy.append(ma)
    y.append(energy/sims)
    
    #print()
    
plt.plot(x,y)
plt.plot(x, maxy)
plt.plot(x, miny)
plt.ylabel("Kinetic energy of the car system at 10 ms-1")
plt.xlabel("Percentage of mass in the wheels")
plt.show()
