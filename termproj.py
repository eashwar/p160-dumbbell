from __future__ import division
from visual import *

scene = display(background=color.white)

# Constants
scale_factor = 2e8 # to make the force vector visible
G = 6.67e-11
pi = 3.141592653

# INITIAL CONDITIONS
iposx = -10 #raw_input("Initial position of bolt - X: ")
iposy = 4 #raw_input("Initial position of bolt - Y: ")
iposz = 0 #raw_input("Initial position of bolt - Z: ")

ivelx = raw_input("Initial velocity of bolt - X: ")
ively = 0 #raw_input("Initial velocity of bolt - Y: ")
ivelz = raw_input("Initial velocity of bolt - Z: ")

initialpos = vector(float(iposx),float(iposy),float(iposz))
print "Initial position: " + str(initialpos)
initialvel = vector(float(ivelx),float(ively),float(ivelz))
print "Initial velocity: " + str(initialvel)

# number of chunks of rod
segments = 2#int(raw_input("Number of segments for volume integral (more is slower): ")) #100 is good

## SPACE ROD
rod = cylinder(pos=(-10,0,0),
                radius=.05,
                axis=(20,0,0),
                mass=pi*pow(.05,2)*20*7850, #7850 kilograms per cubic meter
                color=color.blue)

## SPACE BOLT
bolt = sphere(pos=initialpos,
                   radius=.1,
                   mass=1,
                   color=(0.4,0.4,0.4),
                   make_trail = True)
bolt.velocity = initialvel
bolt.momentum = bolt.mass * bolt.velocity

## FORCE CALCULATION

# the vector
force = vector(0,0,0)
# how long each chunk is
seglength = 2*rod.length/segments
# the mass of each chunk
segmass = (rod.mass/rod.length)*seglength

# the visualization of the force
##gvector = arrow(pos=bolt.pos, axis=scale_factor*force, color=color.red)

# the counter for force calculation
i=0

## TIME
t=0
dt=4

while True:
    rate(50000)

    ## FORCE CALCULATION
    while i < segments:
        segment = vector((-1*(rod.length/2))+(i*seglength),0,0)
        dir_dforce = bolt.pos-segment
        dforce = (-G*segmass*bolt.mass/mag2(dir_dforce))*norm(dir_dforce)
        force += dforce
        i += 1

    ## MOMENTUM PRINCIPLE
    bolt.momentum += force*dt
    bolt.velocity = bolt.momentum/bolt.mass
    bolt.pos += bolt.velocity*dt

    ## FORCE VISUALIZATION UPDATE
##    gvector.pos = bolt.pos
##    gvector.axis = scale_factor*force

    ## RESET COUNTERS/INCREMENT TIME
    force = vector(0,0,0)
    i = 0
    t += dt
