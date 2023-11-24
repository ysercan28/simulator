import json
import random
from time import sleep
import math
from itertools import combinations, permutations

COLLIDE_THRESHOLD = 5
PROC_TICKS = 1000
PARTICLE_COUNT = 100
G = 0.000005#0.000001
C = 100
BOUNDS = [-4096,4096] # pos bounds
MAX_MASS = 100# m bounds
particle_count_per_tick = []
particles = []
time = []  # structure -> [(particles), ...]


def C_limit(v):
    global C
    if v < 0: return -1* min(abs(v), C)
    else: return min(v, C)
    
def calc_gravitational_force(mass1, mass2, distance):
    """
    Calculate gravitational force between two masses in a 1D space.
    """
    
    global G
    try:
        force = G * mass1 * mass2
    except ZeroDivisionError:
        force = 0
    return force

# calculate acceleration
def a(F,m):
    return F/m

def populate_init(particle_count):
    """
    randomly populate the initial position and velocity of a given n of particles 
    """
    for i in range(particle_count):
        pos = [random.randint(BOUNDS[0], BOUNDS[1])]
        vel = [0]
        mass = [random.randint(1, MAX_MASS)]
        particles.append([pos, vel, mass])

def tick():
    global particles
    """
    Update the position and velocity of all particles
    """
    gravity_calc_queue = combinations(particles, 2)
    for subset in gravity_calc_queue:
        

        particle = subset[0]
        particle2 = subset[1]
        if particle[2][0] <= 0 or particle2[2][0] <= 0:
            continue
        distance = abs(particle[0][0] - particle2[0][0])
        mass1 = particle[2][0]
        pos1 = particle[0][0]
        mass2 = particle2[2][0]
        pos2 = particle2[0][0]
                
        force = calc_gravitational_force(mass1, mass2, distance)

        acceleration_1 = a(force, particle[2][0])
        if pos2 < pos1:
            acceleration_1 *= -1
        #print(f"A1 between (mass: {mass1}, pos: {pos1})", f"and (mass: {mass2}, pos: {pos2})", "with distance", distance, "is", acceleration_1, " (applied to first)")
        particle[1][0] += acceleration_1

        acceleration_2 = a(force, particle2[2][0])
        if pos1 < pos2:
            acceleration_2 *= -1
        #print(f"A2 between (mass: {mass1}, pos: {pos1})", f"and (mass: {mass2}, pos: {pos2})", "with distance", distance, "is", acceleration_2, " (applied to second)")
        particle2[1][0] += acceleration_2

    c = 0
    for i in range(len(particles)):
        
        particle = particles[i]
        particle_destroyed = False
        position = particle[0][0]
        velocity = particle[1][0]
        mass = particle[2][0]

        if mass <= 0:
             continue
        new_position = [position + velocity]
        new_velocity = [C_limit(velocity)]
        new_mass = [mass]

        
        for particle2 in particles:
    
            if abs(particle2[0][0] - new_position[0]) <= COLLIDE_THRESHOLD:
                merged_mass = particle2[2][0] + mass
                if particle2[2][0] > mass:
                    #print(f"Merging to 2nd particle. 1st mass {mass}, 2nd mass {particle2[2][0]}")
                  
                    particles[c][2][0] = 0
                    
                    particles[particles.index(particle2)][2] = [merged_mass]
                    particle_destroyed = True
                    break
                     
         
        if particle_destroyed:
            continue
       
        particles[c] = [new_position, new_velocity, new_mass]
        c += 1
        
    particle_count_per_tick.append(len(particles))
    return particles

populate_init(PARTICLE_COUNT)
time.append(particles.copy())
particle_count_per_tick.append(len(particles))
for i in range(PROC_TICKS):
    tick()
    time.append(particles.copy())


import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
# Determine graph

# X axis
x = []
for i in range(PROC_TICKS+1):
    for j in range(particle_count_per_tick[i-1]):
        x.append(i)

# Y axis
y = []
for i in time: # loop thru all times
    for particle in i: # positions of i 
        pos = particle[0][0]
        y.append(pos) 
        
vel_list = []
# velocities
for i in time:
    for particle in i:
        vel_list.append(particle[1][0])
        
mass_list = []

# masses

for i in time:
    for particle in i:
        mass_list.append(particle[2][0])

# Create scatter plot
df = px.data.iris()
fig = px.scatter(df, x=x, y=y, size=list(mass_list), color= vel_list)

fig.update_xaxes(title_text='time')

# Update y-axis label
fig.update_yaxes(title_text='pos')
fig.update_layout(title_text='Allah Simulation')

fig.show()