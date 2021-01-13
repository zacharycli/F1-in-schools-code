#2d physics sim. i don't need a third dimension. 
print("launching")
import os
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import sys
#changeable
co_lift = 0
co_drag = 0.15
cr_area = 0.1 # in metres squared
b_area = 0.5
co_friction_axle = 0.3
radius_axle = 0.002
radius_wheel = 0.013
mass = 0.05


elements_to_change = [[co_drag, cr_area, 0.3, 0], [co_drag, 0.1, co_friction_axle, 0], [co_drag, 0.1, 0.3, co_lift]]
names_of_elements_to_change = [["Drag Coefficient", "Cross -Sectional Area"], ["Drag Coefficient", "Co-efficient of Axle Friction"], ["Drag Coefficient", "Co-efficient of Lift"]]
#changeable, but you shouldn't
g = -9.81
d_air = 1.225
'''
mass min 50g
wheel min 13mm rad
no constraint on axle sizes.
suggestions:

'''

#thrust curve (very messy)
def thrust_curve(x):
    if x >= 0.3:
        ret =  17*(((((x-0.3)/0.4)**2)+5.3)**(-((x-0.3)/0.4)**2))
    else:
        ret =  17*(50000*((((x-0.3)/0.4)**2)+5.3))**(-((x-0.3)/0.4)**2)
    if ret > 17:
        print(x)
        print(ret)
        sys.exit()
    return ret
def it_broke():
    print(f"x = {x}")
    print(f"xspeed = {xspeed}")
    print(f"xaccel = {xaccel}")
    print(f"thrust = {thrust}")
    print(f"co_drag = {co_drag}")
    print(f"cr_area = {cr_area}")
    print(f"time = {t}")

#hyper parameters
num_calcs = 30        # how many calcs for each differentiation (higher = bettter resolution in x)
max_range = 0.4         # how high is the maximum (higher = greater range in x)
max_range_special = 0.01
specials = [2]
sim_tick = 0.001         # how small a unit of time are we calculating with (lower = better resolution in y)

print("going")
print("each 'step' consists of a series of full simulations of the car's motion over 20 metres for one set of values.")
print("each one is a single row of dots on the graphs produced at the end")
#car moves in positive x direction. y is up, so if ypos > 0, there are issues.
x=[[],[],[]]
y=[[],[],[]]
z = [[],[],[]]
for simulation_count in range(len(elements_to_change)):
    li = elements_to_change[simulation_count].copy()
    ls = names_of_elements_to_change[simulation_count].copy()
    for i in range(num_calcs):
        li[0] = ((max_range*i)/num_calcs)
        for a in range(num_calcs):
            if simulation_count in specials:
                li[simulation_count+1] = ((max_range_special*a)/num_calcs)
            else:
                li[simulation_count+1] = ((max_range*a)/num_calcs)
            co_drag = li[0]
            cr_area = li[1]
            co_friction_axle = li[2]
            co_lift = li[3]
            y[simulation_count].append(li[simulation_count+1])
            x[simulation_count].append(li[0])
            #don't mess
            xaccel = 0
            yaccel = 0
            xspeed = 0
            yspeed = 0
            lxspeed = 0
            lyspeed = 0
            xpos = 0
            ypos = 0
            t = 0
            
            while xpos < 20:
                thrust = thrust_curve(t)
                t += sim_tick
                try:
                    xaccel = (thrust-((0.5*d_air*(abs(xspeed)**1.4)*co_drag*cr_area)*(xspeed/abs(xspeed))+(0.5*co_friction_axle*(abs(xspeed)**1.4)*(radius_axle/radius_wheel)*(xspeed/abs(xspeed)))))/mass
                except ZeroDivisionError:
                    xaccel = (thrust-((0.5*d_air*(abs(xspeed)**1.4)*co_drag*cr_area)+(0.5*co_friction_axle*(abs(xspeed)**1.4)*(radius_axle/radius_wheel))))/mass
                xspeed += xaccel*sim_tick
                xpos += ((xspeed+lxspeed)/2)*sim_tick
                lxspeed = xspeed
                if cr_area*co_drag < 0:
                    print(xaccel, xspeed, xpos, t)
                    print((0.5*d_air*(xspeed**2)*co_drag*cr_area))
                if ypos <= 0:
                    ypos = 0
                    yspeed = 0
                    yaccel = (max(0, ((g*mass)+(0.5*d_air*co_lift*(abs(xspeed)**1.4)*b_area)-(0.5*d_air*(abs(yspeed)**1.4)*co_drag*b_area))))/mass
                else:
                    yaccel = (((g*mass)+(0.5*d_air*co_lift*(abs(xspeed)**1.4)*b_area)-(0.5*d_air*(abs(yspeed)**1.4)*co_drag*b_area)))/mass
                    t=-1
                    break
                yspeed += yaccel*sim_tick
                ypos += ((yspeed+lyspeed)/2)*sim_tick
                ypos = max(0, ypos)
                lyspeed = yspeed
                if xspeed <= 0.2 and t > 1:
                    t = -1
                    break
            if cr_area*co_drag < 0:
                print(cr_area, co_drag, t)
            if simulation_count in specials:
                z[simulation_count].append(t)
            else:
                z[simulation_count].append(t)
            '''
            if round(t, 2)== 0.9:
                print(li[0], li[1], t)
            '''
        print(f"step {(i+1)+simulation_count*num_calcs} of {num_calcs*len(elements_to_change)}")
    print(f"graph {1+simulation_count} of {len(elements_to_change)} ready (will be displayed at the end of calculations)")
for i in range(len(elements_to_change)):
    j = 0
    while j < len(z[i]): 
        if z[i][j] == -1:
            z[i].pop(j)
            x[i].pop(j)
            y[i].pop(j)
        else:
            j+=1
    fig = plt.figure()
    
    ax = plt.axes(projection="3d")
    ax.scatter(x[i],y[i],z[i],color = "r")
    '''
    if i == 0:
        ax.scatter(x[0],y[0],[0.9]*864,color = "b")
    '''
    ax.set_xlabel("Drag Coefficient")
    ax.set_ylabel(names_of_elements_to_change[i][1])
    ax.set_zlabel("Time")
    ax.set_xlim3d([0,max(x[i])])
    ax.set_ylim3d([0,max(y[i])])
    ax.set_zlim3d([max(min(z[i]),0),max(z[i])])
    plt.gcf().canvas.set_window_title(f"Figure {i+1}")
    plt.show()

