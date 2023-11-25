import random
import logging
from helpers import formulas
from itertools import combinations
from time import perf_counter

class World:

    def __init__(self, G, c, collide_threshold, particle_count):
        
        self.G = G
        self.c = c
        self.collide_threshold = collide_threshold
        self.particles = []
        self.time = []  # structure -> [[particles], ...]
        self.particle_count = particle_count
        self.particle_count_per_tick = [] # required to ensure x and y axis is aligned correctly
        self.helpers = formulas.Formulas(c, G)
        logging.info("World initiialized")

    def populate(self, POSITION_BOUNDS, MASS_BOUNDS):
        """
        Populate the world with random particles
        """

        self.particles = [] # reset justin case
        logging.info(f"Populating world with {self.particle_count} particles")

        for i in range(self.particle_count):
            pos = random.randint(POSITION_BOUNDS[0], POSITION_BOUNDS[1])
            vel = 0
            mass = random.randint(MASS_BOUNDS[0], MASS_BOUNDS[1])
            self.particles.append([pos, vel, mass])

        logging.info(f"World populated")

    def tick(self):
        """
        Update the position and velocity of all particles
        """
        g_tick_start = perf_counter()
        gravity_calc_queue = combinations(self.particles, 2)
        for subset in gravity_calc_queue:
            particle = subset[0]
            particle2 = subset[1]

            mass1 = particle[2]
            pos1 = particle[0]
            mass2 = particle2[2]
            pos2 = particle2[0]
            distance = abs(pos1-pos2)

            # ignore massless objects
            if mass1 <= 0 or mass2 <= 0: 
                continue             

            force = self.helpers.calc_gravitational_force(mass1, mass2)

            # Calculate velocity of first particle
            acceleration_1 = self.helpers.a(force, mass1)
            if pos2 < pos1:
                acceleration_1 *= -1 
            # logging.debug(f"A1 between (mass: {mass1}, pos: {pos1})", f"and (mass: {mass2}, pos: {pos2})", "with distance", distance, "is", acceleration_1, " (applied to first)")
            particle[1] += acceleration_1
            particle[1] = self.helpers.c_limit(particle[1])
            # Calculate velocity of second particle
            acceleration_2 = self.helpers.a(force, mass2)
            if pos1 < pos2:
                acceleration_2 *= -1
            # logging.debug(f"A2 between (mass: {mass1}, pos: {pos1})", f"and (mass: {mass2}, pos: {pos2})", "with distance", distance, "is", acceleration_2, " (applied to second)")
            particle2[1] += acceleration_2
            particle2[1] = self.helpers.c_limit(particle2[1])
        # logging.debug("Gravity tick took", perf_counter() - g_tick_start, "seconds")

        m_tick_start = perf_counter()
        c = 0
        
        for i in range(len(self.particles)):
            
            particle = self.particles[i]
            particle_destroyed = False
            position = particle[0]
            velocity = particle[1]
            mass = particle[2]

            if mass <= 0:
                continue

            new_position = position + velocity
            new_velocity = velocity
            new_mass = mass

            j = 0
            for i2 in range(len(self.particles)):
                particle2 = self.particles[i2]
        
                if abs(particle2[0] - new_position) <= self.collide_threshold:
                    merged_mass = particle2[2]+ mass
                    if particle2[2] > mass:
                        logging.debug(f"Merging to 2nd particle. 1st mass {mass}, 2nd mass {particle2[2]}, j: {j}, c: {c}")
                        
                        self.particles[c][2] = 0

                        self.particles[self.particles.index(particle2)][2] = merged_mass
                        particle_destroyed = True
                        break
                j += 1
                        
            new_velocity = self.helpers.c_limit(new_velocity)
            if particle_destroyed:
                c += 1
                continue
            
            self.particles[c] = [new_position, new_velocity, new_mass]
            c += 1
        # logging.debug(f"Mass tick took {perf_counter() - m_tick_start} seconds")

    def run(self, PROC_TICKS):
        """
        Run the simulation for PROC_TICKS ticks
        """
        self.time.append(self.particles.copy()) # add initial positions to time as well

        logging.info(f"Running simulation for {PROC_TICKS} ticks")
        
        for i in range(PROC_TICKS):
            self.tick()
            self.particle_count_per_tick.append(len(self.particles))
            self.time.append(self.particles.copy())

        logging.info(f"All ticks finished")
            
