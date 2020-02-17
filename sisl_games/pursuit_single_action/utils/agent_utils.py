import numpy as np

from six.moves import xrange

from .discrete_agent import DiscreteAgent

#################################################################
# Implements utility functions for multi-agent DRL
#################################################################


def create_agents(nagents, map_matrix, obs_range, flatten=False, randinit=False, constraints=None):
    """
    Initializes the agents on a map (map_matrix)
    -nagents: the number of agents to put on the map
    -randinit: if True will place agents in random, feasible locations
               if False will place all agents at 0
    """
    xs, ys = map_matrix.shape
    agents = []
    expanded_mat = np.zeros((xs+2, ys+2))
    for i in xrange(nagents):
        xinit, yinit = (0, 0)
        if randinit:
            # xinit, yinit = feasible_position(map_matrix, constraints=constraints)
            xinit, yinit = feasible_position_ext(map_matrix, expanded_mat, constraints=constraints)
            ## fill expanded_mat
            expanded_mat[xinit+1, yinit+1] = -1
            expanded_mat[xinit+2, yinit+1] = -1
            expanded_mat[xinit, yinit+1] = -1
            expanded_mat[xinit+1, yinit+2] = -1
            expanded_mat[xinit+1, yinit] = -1
            # print(i, (xinit, yinit))
            # print(expanded_mat)
        agent = DiscreteAgent(xs, ys, map_matrix, obs_range=obs_range, flatten=flatten)
        agent.set_position(xinit, yinit)
        agents.append(agent)
    return agents

def feasible_position_ext(map_matrix, expanded_mat, constraints=None):
    """
    Returns a feasible position on map (map_matrix)
    """
    xs, ys = map_matrix.shape
    loop_count = 0
    while True:
        if constraints is None:
            x = np.random.randint(xs)
            y = np.random.randint(ys)
        else:
            xl, xu = constraints[0]
            yl, yu = constraints[1]
            x = np.random.randint(xl, xu)
            y = np.random.randint(yl, yu)
        if map_matrix[x, y] != -1 and expanded_mat[x+1, y+1] != -1:
            return (x, y)

def feasible_position(map_matrix, constraints=None):
    """
    Returns a feasible position on map (map_matrix)
    """
    xs, ys = map_matrix.shape
    loop_count = 0
    while True:
        if constraints is None:
            x = np.random.randint(xs)
            y = np.random.randint(ys)
        else:
            xl, xu = constraints[0]
            yl, yu = constraints[1]
            x = np.random.randint(xl, xu)
            y = np.random.randint(yl, yu)
        if map_matrix[x, y] != -1:
            return (x, y)


def set_agents(agent_matrix, map_matrix):
    # check input sizes
    if agent_matrix.shape != map_matrix.shape:
        raise ValueError("Agent configuration and map matrix have mis-matched sizes")

    agents = []
    xs, ys = agent_matrix.shape
    for i in xrange(xs):
        for j in xrange(ys):
            n_agents = agent_matrix[i, j]
            if n_agents > 0:
                if map_matrix[i, j] == -1:
                    raise ValueError(
                        "Trying to place an agent into a building: check map matrix and agent configuration")
                agent = DiscreteAgent(xs, ys, map_matrix)
                agent.set_position(i, j)
                agents.append(agent)
    return agents