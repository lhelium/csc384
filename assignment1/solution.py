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
  count = 0
  for box in state.boxes:
    if box not in state.storage:
        count += 1
  return count

def heur_alternate(state):
#IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #heur_manhattan_distance has flaws.
    #Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    #Your function should return a numeric value for the estimate of the distance to the goal.
    return 0

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

  return False

def anytime_gbfs(initial_state, heur_fn, timebound = 10):
#IMPLEMENT
  '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
  '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of anytime greedy best-first search'''
  
  gbfs_search_engine = SearchEngine(strategy='best_first', cc_level='full')
  gbfs_search_engine.init_search(initState=initial_state, goal_fn=sokoban_goal_state, heur_fn=heur_fn, fval_function=None)

  # initialize pruning g_value to infinity to make sure pruning happens in the first iteration
  gbfs_costbound = (float("inf"), float("inf"), float("inf")) # [prune states based on g_value, prune states based on h_value, prune states based on f_value]

  # initialize the timekeeping variables
  start_time = os.times()[0]
  time_remaining = timebound

  # run gbfs once to get a solution, save the solution as the best solution encountered so far
  final_state = gbfs_search_engine.search(timebound=time_remaining, costbound=gbfs_costbound)
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

  return False
