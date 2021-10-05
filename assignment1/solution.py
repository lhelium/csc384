 #   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import os
from typing import final #for time functions
from search import * #for search engines
from sokoban import SokobanState, Direction, PROBLEMS #for Sokoban specific classes and problems

def sokoban_goal_state(state):
  '''
  @return: Whether all boxes are stored.
  '''
  for box in state.boxes:
    if box not in state.storage:
      return False
  return True

def manhattan_distance(x, y):
  # Manhattan distance: given x = (x0, x1) and y = (y0, y1), the Manhattan distance d(x, y) = abs(x0 - y0) + abs(x1 - y1)
  distance = abs(x[0] - y[0]) + abs(x[1] - y[1])
  return distance

def heur_manhattan_distance(state): # autograder.py: 20/20
#IMPLEMENT
    '''admissible sokoban puzzle heuristic: manhattan distance'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #We want an admissible heuristic, which is an optimistic heuristic.
    #It must never overestimate the cost to get from the current state to the goal.
    #The sum of the Manhattan distances between each box that has yet to be stored and the storage point nearest to it is such a heuristic.
    #When calculating distances, assume there are no obstacles on the grid.
    #You should implement this heuristic function exactly, even if it is tempting to improve it.
    #Your function should return a numeric value; this is the estimate of the distance to the goal.

    manhattan_distance_sum = 0
    
    unstored_boxes = state.boxes - state.storage

    for box in unstored_boxes:
      distances = []

      # calculate distance from this box to all storage points, keeping track of all distances
      for storage_point in state.storage:
        distance = manhattan_distance(box, storage_point) 
        distances.append(distance)
      
      # search for the closest storage_point to this box by looking for the smallest distance in distances
      min_distance = min(distances)

      # append the shortest distance to the running sum
      manhattan_distance_sum += min_distance
    
    return manhattan_distance_sum


#SOKOBAN HEURISTICS
def trivial_heuristic(state):
  '''trivial admissible sokoban heuristic'''
  '''INPUT: a sokoban state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''

  # number of boxes that aren't in a storage position (ie: number of boxes which have yet to be moved)
  count = 0
  for box in state.boxes:
    if box not in state.storage:
        count += 1
  return count

def is_cornered(box, xmax, ymax):
    # Check if the box is on the corners of the game board
    
    if (box[0] == 0 and box[1] == 0) or \
       (box[0] == 0 and box[1] == ymax - 1) or \
       (box[0] == xmax - 1 and box[1] == 0) or \
       (box[0] == xmax - 1 and box[1] == ymax - 1): 
           return True
    else:
        return False

def is_pseudo_cornered(loc, xmax, ymax, obstacles):
  # If a box isn't on the edge, check that it isn't 'pseudo-cornered' 
  # AKA: Isn't at a location where the only other free spot is located diagonally across from the current state
  if (loc[0] + 1, loc[1]) in obstacles:
    if (loc[0], loc[1] + 1) in obstacles: # box is in upper-left corner
      return True
    elif (loc[0], loc[1] - 1) in obstacles: # box is in lower left corner
      return True
  
  if (loc[0] - 1, loc[1]) in obstacles:
    if (loc[0], loc[1] + 1) in obstacles: # box is in upper-right corner
      return True
    elif (loc[0], loc[1] - 1) in obstacles: # box is in lower-right corner
      return True
  """
  # box is in upper-left corner
  if (loc[0] + 1, loc[1]) in obstacles and (loc[0], loc[1] + 1) in obstacles:
    return True
  
  # box is in lower left corner
  if (loc[0] + 1, loc[1]) in obstacles and (loc[0], loc[1] - 1) in obstacles:
    return True
 
  # box is in upper-right corner
  if (loc[0] - 1, loc[1]) in obstacles and (loc[0], loc[1] + 1) in obstacles:
    return True
  """
  # box is in lower-right corner
  if (loc[0] - 1, loc[1]) in obstacles and (loc[0], loc[1] - 1) in obstacles:
    return True

  # If a box is on the edge, check that its surrounding positions aren't obstacles
  # Left wall  
  if loc[0] == 0:
    if loc[1] - 1 in obstacles or loc[1] + 1 in obstacles: # on left wall and positions above and below it are obstacles
      return True
  
  # Right wall
  if loc[0] == xmax - 1:
    if loc[1] - 1 in obstacles or loc[1] + 1 in obstacles: # on right wall and positions above and below it are obstacles
      return True

  # Upper wall
  if loc[1] == 0:
    if loc[0] - 1 in obstacles or loc[1] + 1 in obstacles: # on top wall and positions left and right it are obstacles
      return True

  # Lower wall
  if loc[1] == ymax - 1:
    if loc[0] - 1 in obstacles or loc[1] + 1 in obstacles: # on bottom wall and positions left and right it are obstacles
      return True

  return False

def has_storage_on_edge(state, box, axis):
  storage_points = state.storage
  
  # we already know that the box is on one of the edges
  for storage in storage_points:
    if axis == "x":
      # if the storage's x position is the same as the box's x position, then the storage and the box are on the same edge (left or right)
      if storage[0] == box[0]:
        return True
    elif axis == "y":
      # if the storage's x position is the same as the box's x position, then the storage and the box are on the same edge (top or bottom)
      if storage[1] == box[1]:
        return True

    return False

def box_is_stuck(state, obstacles):
    # Note: only boxes can be stuck
    
    stuck = False
    unstored_boxes = list(state.boxes - state.storage)
    obstacles = obstacles.union(state.boxes)
    
    for box in state.boxes:
      if box not in state.storage:
        if stuck:
          return True
        
        # Much like Baby from Dirty Dancing, "Nobody puts (the next state) in a corner!"
        # Because, just like how you can't push on a rope in CIV101, you can't pull on a box in sokoban
        
        # On the puzzle board, there are 2 types of corners
        
        # 1. The box is in one of the corners of the game board
        cornered = is_cornered(box, state.width, state.height)
    
        # 2. The box is surrounded on its adjacent sides by obstacles, such that a robot can't move it without pulling on it (a "pseudo-corner")
        surrounded = is_pseudo_cornered(box, state.width, state.height, obstacles)
        
        # If a box is on the edge of the board, and there aren't any storage locations on the edge of the board, then it's also stuck
        # Because you can't get the box back towards the center of the board
        storage_available_on_x = True
        storage_available_on_y = True
    
        if box[0] == 0 or box[0] == state.width - 1:
          storage_available_on_x = has_storage_on_edge(state, box, "x")
        if box[1] == 0 or box[1] == state.height - 1:
          storage_available_on_y = has_storage_on_edge(state, box, "y")
    
        if cornered or surrounded or not storage_available_on_x or not storage_available_on_y:
          stuck = True  
    
    return False
   
def heur_alternate(state):
#IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #heur_manhattan_distance has flaws.
    #Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    #Your function should return a numeric value for the estimate of the distance to the goal.
    
    cost = 0
    unstored_boxes = list(state.boxes - state.storage)
    available_storage = list(state.storage - state.boxes)

    # Check if the current state is "stuck"
    # A box is stuck if it's either cornered or on the edge with no storage boxes located on that edge
    if box_is_stuck(state, state.obstacles):
      # A "stuck" position isn't ideal, so set the cost to be high
      cost += float("inf")
    
    # total cost of optimal path for robot r to move box b to storage point s = cost of optimal path from r to b + cost of optimal path from b to s
    # Split the problem into:
 
    # 1. Finding the closest robot to every box using Manhattan distance
    rb_cost = 0
    
    for box in unstored_boxes:
      distances = []

      for robot in state.robots:
        distance = manhattan_distance(box, robot) 
        distances.append(distance)
      
      min_distance = min(distances)
      rb_cost += min_distance
    
    # 2. Finding the closest storage point to every box using Manhattan distance
    bs_cost = 0
    
    for box in unstored_boxes:
      distances = []

      for storage in available_storage:
        distance = manhattan_distance(box, storage) 
        distances.append(distance)
      
      min_distance = min(distances)
      bs_cost += min_distance
    
    # 3. Sum the costs
    cost += (bs_cost + rb_cost)
        
    return cost

def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0

def fval_function(sN, weight): # autograder.py: 3/3
#IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.
    Use this function stub to encode the standard form of weighted A* (i.e. g + w*h)

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
  
    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.

    fval = sN.gval + (weight * sN.hval)
    return fval

def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound = 10):
#IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of anytime weighted astar algorithm'''
    
    decrease_weight = 0.6
    best_solution = None
    wrapped_fval_function = (lambda sN : fval_function(sN, weight))
	
    astar_search_engine = SearchEngine(strategy='custom', cc_level='full')
    astar_search_engine.init_search(initState=initial_state, goal_fn=sokoban_goal_state, heur_fn=heur_fn, fval_function=wrapped_fval_function)
	  
    # initialize pruning values to infinity to make sure pruning happens in the first iteration
    astar_costbound = (float("inf"), float("inf"), float("inf"))
	
    # initialize the timekeeping variables
    start_time = os.times()[0]
    time_remaining = timebound
	
    while time_remaining > 0:
      final_state = astar_search_engine.search(timebound=time_remaining, costbound=astar_costbound)[0]
      
      if final_state:
          final_state_hval = heur_fn(final_state)
          final_state_fval = final_state.gval + final_state_hval
          
          if final_state_fval < astar_costbound[2]:
              search_time = os.times()[0] - start_time
              time_remaining -= search_time
              start_time = os.times()[0]
              
              # update costbound to reflect the new g_value to prune with
              astar_costbound = (float("inf"), float("inf"), final_state.gval)
              best_solution = final_state
              
              # decrease weight by re-init_search-ing the search engine
              weight *= decrease_weight
              astar_search_engine.init_search(initState=initial_state, goal_fn=sokoban_goal_state, heur_fn=heur_fn, fval_function=wrapped_fval_function)
      else:
          return best_solution  

    return best_solution

def anytime_gbfs(initial_state, heur_fn, timebound = 10): 
#IMPLEMENT
    '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of anytime greedy best-first search'''
    best_solution = None
    
    gbfs_search_engine = SearchEngine(strategy='best_first', cc_level='default')
    gbfs_search_engine.init_search(initState=initial_state, goal_fn=sokoban_goal_state, heur_fn=heur_fn, fval_function=None)

    # initialize pruning g_value to infinity to make sure pruning happens in the first iteration
    gbfs_costbound = (float("inf"), float("inf"), float("inf"))

    # initialize the timekeeping variables
    start_time = os.times()[0]
    time_remaining = timebound

    while time_remaining > 0:
      final_state = gbfs_search_engine.search(timebound=time_remaining, costbound=gbfs_costbound)[0]
      
      if final_state:
          if final_state.gval < gbfs_costbound[0]:
              # deduct search time from the time remaining and reset start_time counter
              search_time = os.times()[0] - start_time
              time_remaining -= search_time
              start_time = os.times()[0]
          
              # update costbound to reflect the new g_value to prune with
              gbfs_costbound = (final_state.gval, float("inf"), float("inf"))
    
              # save the most recent result (which is also the best result)
              best_solution = final_state
      else:
          return best_solution

    return best_solution
