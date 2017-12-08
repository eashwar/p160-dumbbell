from __future__ import division
from visual import *
from visual.graph import *

## Constants
G = 6.67408e-11 #cubic meters per kilogram seconds-squared (m**3 kg**-1 s**-2)
kilo = 1000
mega = 1e6 ## this is used when we have "thousands of kilometers"
exa = 1e18 ## using this for masses

# CUSTOMIZATION

## Scene Parameters
sceneHeight = 900
sceneAspect = 16/9
scene = display(x=10, y=50, width=sceneHeight*sceneAspect, height=sceneHeight, background=color.white)
dumbbellColor = vector(.4,.4,.4)
tightColor = vector(.5 + random.random()*.5,0,.5 + random.random()) # random purple
looseColor = vector(0,.5 + random.random()*.5,5 + random.random()) # random cyan

graph = gdisplay(x=10, y=100+sceneHeight,
                 xtitle='time (weeks)', ytitle='x (meters)',
                 width=sceneHeight*sceneAspect, height=sceneHeight,
                 background=color.white, foreground=color.white)
curve = gcurve(display=graph, color=tightColor)

## System Parameters
dumbbellRad = 5*mega #5000 kilometers
orbitingRad = 1*mega #1000 kilometers

rodLength = 40*mega  #40000 kilometers

dumbbellMass = 200*exa #2e20 kilograms
tightMass = 1*exa     #1e18 kilograms
looseMass = 10*exa     #5e18 kilograms


y_t_init = 15*mega
y_l_init = 35*mega

tightVel = vector(10,0,30)
looseVel = vector(-2,0,10)

# 3D MODELLING

## Dumbbell

### End One
end_one = sphere(pos=(-20*mega,0,0),
                 radius=dumbbellRad,
                 mass=dumbbellMass,
                 color=dumbbellColor)
end_one.velocity = vector(0,0,0)
end_one.momentum = end_one.mass * end_one.velocity

### End Two
end_two = sphere(pos=(20*mega,0,0),
                 radius=dumbbellRad,
                 mass=dumbbellMass,
                 color=dumbbellColor)
end_two.velocity = vector(0,0,0)
end_two.momentum = end_two.mass * end_two.velocity

### Center of Mass
com = sphere(pos=(0,0,0),
             radius=1.3*mega,
             color=color.black)

### Moment Calculation using parallel axis theorem
moment_one = .4*end_one.mass*(end_one.radius**2) + end_one.mass*mag2(com.pos-end_one.pos)
moment_two = .4*end_two.mass*(end_two.radius**2) + end_two.mass*mag2(com.pos-end_two.pos)
net_moment = moment_one+moment_two

### Rod
rod = cylinder(pos=(-20*mega,0,0),
               axis=(rodLength,0,0),
               radius=1.25*mega,
               moment=net_moment,
               color=dumbbellColor)
rod.ang_vel = vector(0,0,0)
rod.ang_mom = rod.ang_vel * rod.moment

dumbbell_angle = 0

## Orbiting bodies

tight = sphere(pos=(-20*mega, y_t_init, 0),
                 radius=1*mega, 
                 mass=1*exa,
                 color=tightColor, make_trail=True)
tight.velocity = tightVel
tight.momentum = tight.mass * tight.velocity


loose = sphere(pos=(0, y_l_init, 0),
                radius=1*mega,
                mass=5*exa,
                color=looseColor, make_trail=True)
loose.velocity = looseVel
loose.momentum = loose.mass * loose.velocity

# TIME
t = 0
dt = 100
   
while (t/604800) <= 1000.0:
    rate(40000)

    if (t%86400 == 0):
        curve.plot(pos=(t/604800, tight.pos.x))

    if (t%604800 == 0):
        print str(t/604800) + " weeks have passed"

        
    #FORCE AND TORQUE CALCULATION
    
    ## Tightly Orbiting Body
    F_tight_one = -1 * norm(tight.pos-end_one.pos) * G * tight.mass * end_one.mass / mag2(tight.pos-end_one.pos)
    F_tight_two = -1 * norm(tight.pos-end_two.pos) * G * tight.mass * end_two.mass / mag2(tight.pos-end_two.pos)
    F_tight_loose = -1 * norm(tight.pos-loose.pos) * G * tight.mass * loose.mass / mag2(tight.pos-loose.pos)
    F_tight_net = F_tight_one + F_tight_two + F_tight_loose

    ## Loosely Orbiting Body
    F_loose_one = -1 * norm(loose.pos-end_one.pos) * G * loose.mass * end_one.mass / mag2(loose.pos-end_one.pos)
    F_loose_two = -1 * norm(loose.pos-end_two.pos) * G * loose.mass * end_two.mass / mag2(loose.pos-end_two.pos)
    F_loose_tight = -1 * norm(loose.pos-tight.pos) * G * loose.mass * tight.mass / mag2(loose.pos-tight.pos)
    F_loose_net = F_loose_one + F_loose_two + F_loose_tight

    ## Dumbbell

    ### End One
    F_one_tight = -1 * norm(end_one.pos-tight.pos) * G * end_one.mass * tight.mass / mag2(end_one.pos-tight.pos)
    F_one_loose = -1 * norm(end_one.pos-loose.pos) * G * end_one.mass * loose.mass / mag2(end_one.pos-loose.pos)
    F_one_net = F_one_tight + F_one_loose
    moment_one = .4*end_one.mass*(end_one.radius**2) + end_one.mass*mag2(com.pos-end_one.pos)
    T_one = cross(F_one_net, end_one.pos-com.pos)


    ### End Two
    F_two_tight = -1 * norm(end_two.pos-tight.pos) * G * end_two.mass * tight.mass / mag2(end_two.pos-tight.pos)
    F_two_loose = -1 * norm(end_two.pos-loose.pos) * G * end_two.mass * loose.mass / mag2(end_two.pos-loose.pos)
    F_two_net = F_two_tight + F_two_loose
    moment_two = .4*end_two.mass*(end_two.radius**2) + end_two.mass*mag2(com.pos-end_two.pos)    
    T_two = cross(F_two_net, end_two.pos-com.pos)

    ### The entire dumbbell
    F_dumbbell = F_one_net + F_two_net
    rod.moment = moment_one+moment_two
    T_net = T_one + T_two


    #MOMENTUM PRINCIPLE

    ## Tightly Orbiting Body
    tight.momentum += F_tight_net*dt
    tight.velocity = tight.momentum/tight.mass
    tight.pos += tight.velocity*dt

    ## Loosely Orbiting Body
    loose.momentum += F_loose_net*dt
    loose.velocity = loose.momentum/loose.mass
    loose.pos += loose.velocity*dt

    ## Dumbbell
    
    ### Linear
    com.pos = ((end_one.pos*end_one.mass) + (end_two.pos*end_two.mass))/(end_one.mass+end_two.mass)
    end_one.momentum += F_dumbbell*dt
    end_one.velocity = end_one.momentum/end_one.mass
    end_one.pos += end_one.velocity*dt

    rod.pos = end_one.pos
    
    end_two.momentum += F_dumbbell*dt
    end_two.velocity = end_two.momentum/end_two.mass
    end_two.pos += end_two.velocity*dt
    
    ### Angular
    rod.ang_mom += T_net*dt
    rod.ang_vel = rod.ang_mom/rod.moment

    dumbbell_angle = -mag(rod.ang_vel)*dt
    
    rod.rotate(angle=dumbbell_angle, axis=rod.ang_vel, origin=com.pos)
    end_one.rotate(angle=dumbbell_angle, axis=rod.ang_vel, origin=com.pos)
    end_two.rotate(angle=dumbbell_angle, axis=rod.ang_vel, origin=com.pos)


    t += dt
