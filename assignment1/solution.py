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

def heur_manhattan_distance(state):
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

    for box in state.boxes:
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

# NOTE THAT ONLY BOXES CAN BE STUCK, robots can move in the backwards direction 
# NEED TO DECIDE: do you want to call this function with only state (ie: call it once only)
# or call it for every box
# also decide if you want to keep changing_obstacles bc idk if it's actually doing anything
def box_is_stuck(state, box, obstacles, changing_obstacles):
  # A box is stuck if it's either cornered or on the edge with no storage boxes located on that edge

  # Just like how you can't push on a rope in CIV101, you can't pull on a box in CSC384 A1
  # Therefore, if a box is on the edge of the board, and there aren't any storage locations on the edge of the board, then the position isn't admissible
  # Because you can't get the box back towards the center of the board

  cornered = is_cornered(box, obstacles, changing_obstacles)

  edged_out = has_storage_on_x(state, box) or has_storage_on_y(state, box)

  if edged_out or cornered:
    return True
  else:
    return False

def is_cornered(loc, obstacles, changing_obstacles):
  # Much like Baby from Dirty Dancing, "Nobody puts (the next state) in a corner!"
  # A 'corner' is defined as the a location where the only other free spot is located diagonally across from the current state

  if (loc[0] + 1, loc[1]) in obstacles or (loc[0] + 1, loc[1]) in changing_obstacles:
    if (loc[0], loc[1] + 1) in obstacles or (loc[0], loc[1] + 1) in changing_obstacles: # upper-left corner
      return True
    elif (loc[0], loc[1] - 1) in obstacles or (loc[0], loc[1] - 1) in changing_obstacles: # lower left corner
      return True
    else:
      return False
  
  if (loc[0] - 1, loc[1]) in obstacles or (loc[0] - 1, loc[1]) in changing_obstacles:
    if (loc[0], loc[1] + 1) in obstacles or (loc[0], loc[1] + 1) in changing_obstacles: # upper-right corner
      return True
    elif (loc[0], loc[1] - 1) in obstacles or (loc[0], loc[1] - 1) in changing_obstacles: # lower-right corner
      return True
    else:
      return False
  
def has_storage_on_x(state, box):
  storage_points = state.storage()
  for storage in storage_points:
    # if the storage's x position is the same as the box's x position, then the storage and the box are on the same edge (left or right)
    if storage[0] == box[0]:
      return True

    return False

def has_storage_on_y(state, box):
  storage_points = state.storage()
  for storage in storage_points:
    # if the storage's x position is the same as the box's x position, then the storage and the box are on the same edge (top or bottom)
    if storage[1] == box[1]:
      return True

    return False

def heur_alternate(state):
#IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #heur_manhattan_distance has flaws.
    #Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    #Your function should return a numeric value for the estimate of the distance to the goal.

    count = 0
    unstored_boxes = state.boxes - state.storage
    available_storage = state.storage - state.boxes

    # Find the location of the obstacles
    # Obstacles include: boundaries of the board, other robots (added dynamically), other boxes (added dynamically), actual obstacles themselves
    obstacles = [] 

    for x in range(-1, state.width + 1):
      obstacles.append((x, -1)) # upper wall
      obstacles.append((x, state.height + 1)) # lower wall

    for y in range(state.height):
      obstacles.append((-1, y)) # left wall
      obstacles.append(state.width + 1, y) # right wall
    
    for obstacle in state.obstacles:
      obstacles.append(obstacle)

    # total cost of optimal path for robot r to move box b to storage point s = cost of optimal path from r to b + cost of optimal path from b to s
    # Split the problem into:
    # 1. Finding the cost of the path from every robot to every box
    # 2. Finding the cost of the path from every box to every storage point

    # Let the path from start to goal be represented as: start -> next -> ... -> goal
    # Assumption: if start -> next is legal (ie: next isn't an obstacle) and admissible (ie: next isn't cornered in), then every move from next -> goal is legal and admissible

    # Just like how you can't push on a rope in CIV101, you can't pull on a box in CSC384 A1
    # Therefore, if a box is on the edge of the board, and there aren't any storage locations on the edge of the board, then the position isn't admissible

    # 1. Finding the cost of the path from every robot to every box
    rb_cost = 0
    for robot in state.robots:
      dist_from_box = []
      for box in unstored_boxes:
        changing_obstacles = (state.robots - robot) + (state.boxes - state.storage - box)
        if box_is_stuck(state, box, obstacles, changing_obstacles):
          rb_cost += 1000
        else:
          distance = abs(box[0] - robot[0]) + abs(box[1] - robot[1])
          dist_from_box.append(distance)
      
      min_distance = min(dist_from_box)
      rb_cost += min_distance
    
    # 2. Finding the cost of the path from every box to every storage point
    bs_cost = 0
    for box in unstored_boxes:
      dist_from_box = []
      for storage in available_storage:
        distance = abs(box[0] - storage[0]) + abs(box[1] - storage[1])
        dist_from_box[storage] = distance
      
      min_distance = min(dist_from_box)
      bs_cost += min_distance

    return count

def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0

def fval_function(sN, weight):
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

  wrapped_fval_function = (lambda sN : fval_function(sN, weight))

  astar_search_engine = SearchEngine(strategy='custom', cc_level='full')
  astar_search_engine.init_search(initial_state=initial_state, goal_fn=sokoban_goal_state, heur_fn=heur_fn, fval_function=wrapped_fval_function)
  
  # initialize pruning values to infinity to make sure pruning happens in the first iteration
  astar_costbound = (float("inf"), float("inf"), float("inf"))

  # initialize the timekeeping variables
  start_time = os.times()[0]
  time_remaining = timebound

  # run A* once to get a solution
  final_state = astar_search_engine.search(timebound=time_remaining, costbound=astar_costbound)
  if not final_state:
    best_solution = False
  else:
    best_solution = final_state

  while time_remaining > 0:
    # if the search doesn't return anything, return from the function
    if not final_state:
      return best_solution
    
    # only search if current solution's gval+hval is less than the gval specified in costbound
    if (final_state.gval + final_state.hval) < astar_costbound[0]:
      # deduct search time from the time remaining and reset start_time counter
      search_time = os.times()[0] - start_time
      time_remaining -= search_time
      start_time = os.times()

      # update costbound to reflect the new g_value to prune with
      astar_costbound = (final_state.gval, float("inf"), float("inf"))

      # save the most recent result (which is also the best result)
      best_solution = final_state
    
    else:
      # gbfs couldn't find a path with lower gval than the gval of the previous search iteration
      # so best_solution is indeed the best solution
      return best_solution
    
    #decrease_weight = 0.8
    #weight *= decrease_weight
    # I think the weight should be decreased each time but no function takes in the weight after the init_search function?
    # So how do you actually decrease the weight in each iteration?

    final_state = astar_search_engine.search(timebound=time_remaining, costbound=astar_costbound)

  return best_solution

def anytime_gbfs(initial_state, heur_fn, timebound = 10):
#IMPLEMENT
  '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
  '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of anytime greedy best-first search'''
  
  gbfs_search_engine = SearchEngine(strategy='best_first', cc_level='full')
  gbfs_search_engine.init_search(initState=initial_state, goal_fn=sokoban_goal_state, heur_fn=heur_fn, fval_function=None)

  # initialize pruning g_value to infinity to make sure pruning happens in the first iteration
  gbfs_costbound = (float("inf"), float("inf"), float("inf"))

  # initialize the timekeeping variables
  start_time = os.times()[0]
  time_remaining = timebound

  # run gbfs once to get a solution, save the solution as the best solution encountered so far
  final_state = gbfs_search_engine.search(timebound=time_remaining, costbound=gbfs_costbound)
  if not final_state:
    best_solution = False
  else:
    best_solution = final_state

  while time_remaining > 0:
    # if the search doesn't return anything, return from the function
    if not final_state:
      return best_solution
    
    # only search if current solution's gval is less than the gval specified in costbound
    if final_state.gval < gbfs_costbound[0]:
      # deduct search time from the time remaining and reset start_time counter
      search_time = os.times()[0] - start_time
      time_remaining -= search_time
      start_time = os.times()

      # update costbound to reflect the new g_value to prune with
      gbfs_costbound = (final_state.gval, float("inf"), float("inf"))

      # save the most recent result (which is also the best result)
      best_solution = final_state
    
    else:
      # gbfs couldn't find a path with lower gval than the gval of the previous search iteration
      # so best_solution is indeed the best solution
      return best_solution
    
    final_state = gbfs_search_engine.search(timebound=time_remaining, costbound=gbfs_costbound)

  return best_solution
