def thrust_curve(x):
    if x >= 0.3:
        ret =  6*(((((x-0.3)/0.4)**2)+5.3)**(-((x-0.3)/0.4)**2))
    else:
        ret =  6*(50000*((((x-0.3)/0.4)**2)+5.3))**(-((x-0.3)/0.4)**2)
    return ret
co_lift = 0.00005
b_area = 0.5
force = 0.222260994 #drag force given in newtons from ansys at 20 ms-1
cr_area = 1570*(1/(1000**2)) # frontal area in metres squared
co_drag = (force*2)/(1.225*cr_area*20) #drag co-efficient
co_friction_axle = 0.01
radius_axle = 0.001
radius_wheel = 0.013
mass = 0.05
sim_tick = 0.000001
g = -9.81
d_air = 1.225
xspeed = 0
yspeed = 0
lxspeed = 0
lyspeed = 0
xpos = 0
ypos = 0
t = 0
mxspeed = 0
print("Simulating...")#the simulator takes into account air resistance, varying thrust profiles and axle friction. but we don't know the exact thrust profile, so the one used is an informed guess
while xpos < 20:
    t += sim_tick
    thrust = thrust_curve(t)
    try:
        xaccel = (thrust-((0.5*d_air*(abs(xspeed)**1.4)*co_drag*cr_area)*(xspeed/abs(xspeed))+(0.5*co_friction_axle*(abs(xspeed)**1.4)*(radius_axle/radius_wheel)*(xspeed/abs(xspeed)))))/mass
    except ZeroDivisionError:
        xaccel = (thrust-((0.5*d_air*(abs(xspeed)**1.4)*co_drag*cr_area)+(0.5*co_friction_axle*(abs(xspeed)**1.4)*(radius_axle/radius_wheel))))/mass
    xspeed += xaccel*sim_tick
    xpos += ((xspeed+lxspeed)/2)*sim_tick
    lxspeed = xspeed
    if xspeed > mxspeed:
        mxspeed = xspeed
    if ypos <= 0:
        ypos = 0
        yspeed = 0
        yaccel = (max(0, ((g*mass)+(0.5*d_air*co_lift*(abs(xspeed)**1.4)*b_area)-(0.5*d_air*(abs(yspeed)**1.4)*co_drag*b_area))))/mass
    else:
        yaccel = (((g*mass)+(0.5*d_air*co_lift*(abs(xspeed)**1.4)*b_area)-(0.5*d_air*(abs(yspeed)**1.4)*co_drag*b_area)))/mass
        print("Car took off.")
        break
    yspeed += yaccel*sim_tick
    ypos += ((yspeed+lyspeed)/2)*sim_tick
    ypos = max(0, ypos)
    lyspeed = yspeed
print(f"time: {t}s")
print(f"max speed: {mxspeed} ms-1")

