from modals import World
import constants
import logging,sys

G = constants.G
c = constants.c
POS_BOUNDS = constants.POS_BOUNDS
MASS_BOUNDS = constants.MASS_BOUNDS
PARTICLE_COUNT = constants.PARTICLE_COUNT
PROC_TICKS = constants.PROC_TICKS
COLLIDE_THRESHOLD = constants.COLLIDE_THRESHOLD

logging.basicConfig(filename="log.log", level=logging.DEBUG)

if __name__ == "__main__":
    print("Running simulation...")
    simulation = World.World(G, c, COLLIDE_THRESHOLD, PARTICLE_COUNT)
    simulation.populate(POS_BOUNDS, MASS_BOUNDS)
    simulation.run(PROC_TICKS) # simulate for x ticks

    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import plotly.express as px
    # Determine graph

    # X axis
    x = []
    for i in range(PROC_TICKS+1):
        for j in range(simulation.particle_count_per_tick[i-1]):
            x.append(i)

    # Y axis
    y = []
    for i in simulation.time: # loop thru all times
        for particle in i: # positions of i 
            pos = particle[0]
            y.append(pos) 
            
    vel_list = []
    # velocities
    for i in simulation.time:
        for particle in i:
            vel_list.append(particle[1])
            
    mass_list = []

    # masses

    for i in simulation.time:
        for particle in i:
            mass_list.append(particle[2])

    # Create scatter plot
    df = px.data.iris()
    fig = px.scatter(df, x=x, y=y, size=list(mass_list), color= vel_list)

    fig.update_xaxes(title_text='time')

    # Update y-axis label
    fig.update_yaxes(title_text='pos')
    fig.update_layout(title_text='Allah Simulation')

    fig.show()