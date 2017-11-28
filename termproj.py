from __future__ import division
from visual import *

## Constants
G = 6.67408e-11 #cubic meters per kilogram seconds-squared (m**3 kg**-1 s**-2)
kilo = 1000
mega = 1e6 ## this is used when we have "thousands of kilometers"
exa = 1e18 ## using this for masses

# CUSTOMIZATION

## Scene Parameters
sceneWidth = 1200
sceneAspect = 1/1
scene = display(x=10, y=50, width=sceneWidth, height=sceneWidth*sceneAspect, background=color.white)
dumbbellColor = vector(.4,.4,.4)
tightColor = vector(.5 + random.random()*.5,0,.5 + random.random())
looseColor = vector(0,.5 + random.random()*.5,5 + random.random())


## System Parameters
dumbbellRad = 5*mega #5000 kilometers
orbitingRad = 1*mega #1000 kilometers

rodLength = 40*mega  #40000 kilometers

dumbbellMass = 200*exa #5e19 kilograms
tightMass = 1*exa     #1e18 kilograms
looseMass = 5*exa     #5e18 kilograms

dumbbellVelocity = vector(0,0,0)

# 3D MODELLING

## Dumbbell

### End One
end_one = sphere(pos=(-20*mega,0,0),
                 radius=dumbbellRad,
                 mass=dumbbellMass,
                 color=dumbbellColor)
end_one.velocity = dumbbellVelocity
end_one.momentum = end_one.mass * end_one.velocity

### End Two
end_two = sphere(pos=(20*mega,0,0),
                 radius=dumbbellRad,
                 mass=dumbbellMass,
                 color=dumbbellColor)
end_two.velocity = dumbbellVelocity
end_two.momentum = end_two.mass * end_two.velocity

### Center of Mass
com = sphere(pos=(0,0,0),
             radius=1.3*mega,
             color=color.black)

### Moment Calculation
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

tight = sphere(pos=(-20*mega, 30*mega, 0),
                 radius=1*mega, 
                 mass=1*exa,
                 color=tightColor, make_trail=True)

tight.velocity = vector(0,0,0)
tight.momentum = tight.mass * tight.velocity


loose = sphere(pos=(0, 40*mega, 0),
                radius=1*mega,
                mass=5*exa,
                color=looseColor, make_trail=True)

loose.velocity = vector(0,0,7)
loose.momentum = loose.mass * loose.velocity

## TIME
t = 0
dt = 100
   
while True:
    rate(10000)

    #FORCE CALCULATION
    
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
    
    ## End One
    F_one_tight = -1 * norm(end_one.pos-tight.pos) * G * end_one.mass * tight.mass / mag2(end_one.pos-tight.pos)
    F_one_loose = -1 * norm(end_one.pos-loose.pos) * G * end_one.mass * loose.mass / mag2(end_one.pos-loose.pos)
    F_one_net = F_one_tight + F_one_loose

    ## End Two
    F_two_tight = -1 * norm(end_two.pos-tight.pos) * G * end_two.mass * tight.mass / mag2(end_two.pos-tight.pos)
    F_two_loose = -1 * norm(end_two.pos-loose.pos) * G * end_two.mass * loose.mass / mag2(end_two.pos-loose.pos)
    F_two_net = F_two_tight + F_two_loose

    F_dumbbell = F_one_net + F_two_net


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
    ### Linear Momentum Principle
    com.pos = ((end_one.pos*end_one.mass) + (end_two.pos*end_two.mass))/(end_one.mass+end_two.mass)
    end_one.momentum += F_dumbbell*dt
    end_one.velocity = end_one.momentum/end_one.mass
    end_one.pos += end_one.velocity*dt

    rod.pos = end_one.pos
    
    end_two.momentum += F_dumbbell*dt
    end_two.velocity = end_two.momentum/end_two.mass
    end_two.pos += end_two.velocity*dt
    
    ### Angular Momentum Principle
    moment_one = .4*end_one.mass*(end_one.radius**2) + end_one.mass*mag2(com.pos-end_one.pos)
    moment_two = .4*end_two.mass*(end_two.radius**2) + end_two.mass*mag2(com.pos-end_two.pos)
    rod.moment = moment_one+moment_two

    T_one = cross(F_one_net, end_one.pos-com.pos)
    T_two = cross(F_two_net, end_two.pos-com.pos)
    T_net = T_one + T_two
    
    rod.ang_mom += T_net*dt
    rod.ang_vel = rod.ang_mom/rod.moment

    dumbbell_angle += mag(rod.ang_vel)*dt
    
    rod.rotate(angle=dumbbell_angle, axis=rod.ang_vel, origin=com.pos)
    end_one.rotate(angle=dumbbell_angle, axis=rod.ang_vel, origin=com.pos)
    end_two.rotate(angle=dumbbell_angle, axis=rod.ang_vel, origin=com.pos)

    t += dt
