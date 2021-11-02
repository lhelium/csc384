from csp import Constraint, Variable, CSP
from constraints import *
from backtracking import bt_search

##################################################################
### NQUEENS
##################################################################

def nQueens(n, tableCnstr):
    '''Return an n-queens CSP, optionally use tableContraints'''
    i = 0
    dom = []
    for i in range(n):
        dom.append(i+1)

    vars = []
    for i in dom:
        vars.append(Variable('Q{}'.format(i), dom))

    cons = []
    for qi in range(len(dom)):
        for qj in range(qi+1, len(dom)):
            if tableCnstr:
                con = QueensTableConstraint("C(Q{},Q{})".format(qi+1,qj+1),
                                            vars[qi], vars[qj], qi+1, qj+1)
            else: con = QueensConstraint("C(Q{},Q{})".format(qi+1,qj+1),
                                        vars[qi], vars[qj], qi+1, qj+1)
            cons.append(con)

    csp = CSP("{}-Queens".format(n), vars, cons)
    return csp

def solve_nQueens(n, algo, allsolns, tableCnstr=False, variableHeuristic='fixed', trace=False):
    '''Create and solve an nQueens CSP problem. The first
       parameer is 'n' the number of queens in the problem,
       The second specifies the search algorithm to use (one
       of 'BT', 'FC', or 'GAC'), the third specifies if
       all solutions are to be found or just one, variableHeuristic
       specfies how the next variable is to be selected
       'random' at random, 'fixed' in a fixed order, 'mrv'
       minimum remaining values. Finally 'trace' if specified to be
       'True' will generate some output as the search progresses.
    '''
    csp = nQueens(n, tableCnstr)
    solutions, num_nodes = bt_search(algo, csp, variableHeuristic, allsolns, trace)
    print("Explored {} nodes".format(num_nodes))
    if len(solutions) == 0:
        print("No solutions to {} found".format(csp.name()))
    else:
       print("Solutions to {}:".format(csp.name()))
       i = 0
       for s in solutions:
           i += 1
           print("Solution #{}: ".format(i),)
           for (var,val) in s:
               print("{} = {}, ".format(var.name(),val),)
           print("")

##################################################################
### SUDOKU
##################################################################

def sudokuCSP(initial_sudoku_board, model='neq'):
    '''The input board is specified as a list of 9 lists. Each of the
       9 lists represents a row of the board. If a 0 is in the list it
       represents an empty cell. Otherwise if a number between 1--9 is
       in the list then this represents a pre-set board
       position. E.g., the board

       -------------------
       | | |2| |9| | |6| |
       | |4| | | |1| | |8|
       | |7| |4|2| | | |3|
       |5| | | | | |3| | |
       | | |1| |6| |5| | |
       | | |3| | | | | |6|
       |1| | | |5|7| |4| |
       |6| | |9| | | |2| |
       | |2| | |8| |1| | |
       -------------------
       would be represented by the list of lists

       [[0,0,2,0,9,0,0,6,0],
       [0,4,0,0,0,1,0,0,8],
       [0,7,0,4,2,0,0,0,3],
       [5,0,0,0,0,0,3,0,0],
       [0,0,1,0,6,0,5,0,0],
       [0,0,3,0,0,0,0,0,6],
       [1,0,0,0,5,7,0,4,0],
       [6,0,0,9,0,0,0,2,0],
       [0,2,0,0,8,0,1,0,0]]


       Construct and return CSP for solving this sudoku board using
       binary not equals if model='neq' or using allDiff constraints
       if model='alldiff'

       The CSP contains a variable for each cell of the board with
       with domain equal to {1-9} if the board has a 0 at that position,
       and domain equal {i} if the board has a fixed number i at that
       cell.

       The CSP has a neq constraint between every relevant pair of
       varibles, or an alldiff constraint between every set of
       variables in a row, column, or sub-square

    '''
    #your implementation for Question 4 changes this function
    #implement handling of model == 'alldiff'

    if not model in ['neq', 'alldiff']:
        print("Error wrong sudoku model specified {}. Must be one of {}".format(
            model, ['neq', 'alldiff']))

    #first define the variables
    i = 0
    var_array = []

    for row_list in initial_sudoku_board:
        var_array.append([])
        j = 0
        
        for col in row_list:
            cell = initial_sudoku_board[i][j]
            
            if cell == 0:
                dom = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            else:
                dom = [cell]
            
            var = Variable("V{},{}".format(i+1, j+1), dom)
            var_array[i].append(var)
            j += 1
        
        i += 1

    #Set up the constraints
    #row constraints
    constraint_list = []

    for row in var_array:
        if model == 'neq':
            constraint_list.extend(post_all_pairs(row))
        elif model == 'alldiff':
            # TO IMPLEMENT
            #util.raiseNotDefined()
            # constraints.AllDiffConstraint(self, name, scope)
            # note that scope is the same scope as 'neq' above
            row_num = var_array.index(row)
            cnstrs = AllDiffConstraint('sudoku_row_' + str(row_num), row)
            constraint_list.extend([cnstrs])

    for colj in range(len(var_array[0])):
        scope = list(map(lambda row: row[colj], var_array))
        
        if model == 'neq':
            constraint_list.extend(post_all_pairs(scope))
        elif model == 'alldiff':
            # TO IMPLEMENT
            #util.raiseNotDefined()
            cnstrs = AllDiffConstraint('sudoku_col_' + str(colj), scope)
            constraint_list.extend([cnstrs])

    for i in [0, 3, 6]:
        for j in [0, 3, 6]:
            #initial upper left hand index of subsquare
            scope = []
            
            for k in [0, 1, 2]:
                for l in [0,1,2]:
                    scope.append(var_array[i+k][j+l])
            
            if model == 'neq':
                constraint_list.extend(post_all_pairs(scope))
            elif model == 'alldiff':
                # TO IMPLEMENT
                #util.raiseNotDefined()
                cnstrs = AllDiffConstraint('sudoku_subsquare_' + str(int(i/3)) + '_' + str(int(j/3)), scope)
                constraint_list.extend([cnstrs])

    vars = [var for row in var_array for var in row]
    
    return CSP("Sudoku", vars, constraint_list)

def post_all_pairs(var_list):
    '''create a not equal constraint between all pairs of variables in var_list
       return list of constructed constraint objects'''
    constraints = []
    for i in range(len(var_list)):
        for j in range(i+1,len(var_list)):
            c = NeqConstraint("({},{})".format(var_list[i].name(), var_list[j].name()),[var_list[i], var_list[j]])
            constraints.append(c)
    return constraints

def solve_sudoku(initialBoard, model, algo, allsolns,
                 variableHeuristic='fixed', trace=False):
    if not model in ['neq', 'alldiff']:
        print("Error wrong sudoku model specified {}. Must be one of {}".format(
            model, ['neq', 'alldiff']))
    csp = sudokuCSP(initialBoard, model)

    solutions, num_nodes = bt_search(algo, csp, variableHeuristic, allsolns, trace)
    print("Explored {} nodes".format(num_nodes))
    if len(solutions) == 0:
        print("No solutions to {} found".format(csp.name()))
    else:
        i = 0
        for s in solutions:
            i += 1
            print("Solution #{}: ".format(i))
            sudoku_print_soln(s)

def sudoku_print_soln(s):
    '''s is a list of (var,value) pairs. Organize them into
       the right order and then print(it in a board layout'''
    s.sort(key=lambda varval_pair: varval_pair[0].name())
    print("-"*37)
    for i in range(0,9):
        print("|", end='')
        for j in range(0,9):
            indx = i*9 + j
            print(s[indx][1], "|", end='')
        print("")
        print("-"*37)


##################################################################
### Plane Sequencing
##################################################################

class PlaneProblem:
    '''Class to hold an instance of the plane scheduling problem.
       defined by the following data items
       a) A list of planes

       b) A list of needed flights

       c) Legal flights for each plane. Specified as a list of lists
          For each list L. L[0] = a particular plane P. and L[1], L[2} ...
          are all of the flights that P is equipped to fly.
          This must be a subset of the list of flights

       d) Possible starting flights for each plane. Specified as a
          list of lists For each list L. L[0] = a particular plane P,
          and L[1], L[2], ...  are all of the flights that in the same
          place the plane that P is initially located. This must be a
          subset of the list of flights. Note however, that that P
          might not be able to fly all of these flights (so the list
          (c) needs to be checked as well)


       e) A list of pairs of flights (f1,f2) such that f2 can legally
          follow f1 in a plane's schedule. (That is, f2 starts at the
          same location that f1 end).

       f) A list of flights that end in a location where maintenance
          can be performed

       g) In integer specifying the minimum frequency of plane
          maintenance. That is, if the minimum frequency is 4, then at
          least one out of every sequence of 4 flights a plane makes
          must be a flight ending at a location where maintenance can
          be performed.

    '''
    def __init__(self, planes, flights, can_fly, flights_at_start,
                 can_follow, maintenance_flights, min_maintenance_frequency):
        self.planes = planes
        self.flights = flights
        self._can_fly = dict()
        self._flights_at_start = dict()
        self.can_follow = can_follow
        self.maintenance_flights = maintenance_flights
        self.min_maintenance_frequency = min_maintenance_frequency

        #do some data checks
        for l in can_fly:
            for f in l[1:]:
                if f not in flights:
                    print("PlaneProblem Error, can_fly contains a non-flight", f)
        for l in flights_at_start:
            for f in l[1:]:
                if f not in flights:
                    print("PplaneProblem Error, flights_at_start contains a non-flight", f)
        for (f1, f2) in can_follow:
            if f1 not in flights or f2 not in flights:
                print("PlaneProblem Error, can_fly contains pair with non-flight (", f1, ",", f2, ")")

        for f in maintenance_flights:
            if f not in flights:
                print("PlaneProblem Error, maintenance_flights fly contains non-flight", f)

        if min_maintenance_frequency == 0:
            print("PlaneProblem Error, min_maintenance_frequency must be greater than 0")

        #now convert can_fly and flights_at_start to a dictionary that
        #can be indexed by the plane.
        for l in can_fly:
            self._can_fly[l[0]] = l[1:]
        for l in flights_at_start:
            self._flights_at_start[l[0]] = l[1:]

        #some useful access functions
    def can_fly(self, plane):
        '''Return list of flights plane can fly'''
        return self._can_fly[plane]

    def can_start(self, plane):
        '''Return list of flights plane can start with'''
        return list(
            set(self._can_fly[plane]).intersection(
                self._flights_at_start[plane]))

def solve_planes(planes_problem, algo, allsolns,
                 variableHeuristic='fixed', silent=False, trace=False):
    #Your implementation for Question 6 goes here.
    #
    #Do not but do not change the functions signature
    #(the autograder will twig out if you do).

    #If the silent parameter is set to True
    #you must ensure that you do not execute any print statements
    #in this function.
    #(else the output of the autograder will become confusing).
    #So if you have any debugging print statements make sure you
    #only execute them "if not silent". (The autograder will call
    #this function with silent=True, plane_scheduling.py will call
    #this function with silent=False)

    #You can optionally ignore the trace parameter
    #If you implemented tracing in your FC and GAC implementations
    #you can set this argument to True for debugging.
    #
    #Once you have implemented this function you should be able to
    #run plane_scheduling.py to solve the test problems (or the autograder).
    #
    #
    '''This function takes a planes_problem (an instance of PlaneProblem
       class) as input. It constructs a CSP, solves the CSP with bt_search
       (using the options passed to it), and then from the set of CSP
       solutions it constructs a list of lists specifying a schedule
       for each plane and returns that list of lists
       The required format is the list of lists is:

       For each plane P the list of lists contains a list L.
       L[0] == P (i.e., the first item of the list is the plane)
       and L[1], ..., L[k] (i.e., L[1:]) is the sequence of flights
       assigned to P.

       The returned list of lists should contain a list for every
       plane.
    '''

    #BUILD your CSP here and store it in the varable csp
    #util.raiseNotDefined()
    def plane_csp(planes_problem):
        # variables: planes (array of length len(flights))
        #     ex: AC-1, AC-2...
        # values: flights 
        #     ex: AC001, AC002, AC003, AC004, AC005
        # domain of possible values: the flights which a plane can fly 
        #     ex: AC-1 can fly any flight, AC-2 can't fly flight AC003 but can fly any other flight
        #     dom(AC-1) = AC001, AC002, AC003, AC004, AC005
        #     dom(AC-2) = AC001, AC002,        AC004, AC005
        # var_array should take the form:
        #     var_array[0][0] = first flight flown by plane AC-1 (initially all flights that can be flown by plane AC-1)
        #     var_array[0][1] = second flight flown by plane AC-1
        #     var_array[0][2] = third flight flown by plane AC-1
        #     var_array[1][0] = first flight flown by plane AC-2 (initially all flights that can be flown by plane AC-2)
        #     etc...

        planes = planes_problem.planes
        flights = planes_problem.flights
        can_fly = planes_problem._can_fly # format: list of dicts {plane_name : [flights]}
        flights_at_start = planes_problem._flights_at_start # format: list of dicts {plane_name : [flights]}
        can_follow = planes_problem.can_follow # format: list of tuples (flight_one, flight_two)
        maintenance_flights = planes_problem.maintenance_flights
        min_maintenance_frequency = planes_problem.min_maintenance_frequency
        
        var_array = []

        # i = which plane
        for i in range(len(planes)):
            var_array.append([])

            plane_can_fly = can_fly[planes[i]]
            plane_can_start = flights_at_start[planes[i]]

            # C1 (unary constraint, can directly modify domain): each plane is only assigned flights it is capable of flying 
            for j in range(len(plane_can_fly)):
                dom = []
                dom.append("none") # since you can have situations like P4 where no flight can be assigned

                # C2 (unary constraint, can directly modify domain): each plane's initial flight can only be a flight departing from that plane's initial location
                if j == 0:
                    valid_flights = [flight for flight in plane_can_fly if flight in plane_can_start]

                    """ for flight in valid_flights:
                        dom.append(flight) """
                    dom.extend(valid_flights)
                    
                else:
                    """ for flight in plane_can_fly:
                        dom.append(flight) """
                    dom.extend(plane_can_fly)
                
                var = Variable("Plane {} Flight number {}".format(planes[i], j), dom)
                var_array[i].append(var)

        # create and add all the constraints
        constraint_list = []

        # C3: sequence of flights flown must be feasible
        # valid_connections stores the satisfying assignments
        valid_connections = []

        # add the valid connection pairs
        for connection in can_follow:
            valid_connections.append(list(connection))
        
        # add connections for the terminal flights (ie: where arrival is "none")
        for flight in flights:
            valid_connections.append([flight, "none"])

        # for planes where no flights are scheduled, no flight -> no flight is a valid connection
        valid_connections.append(["none", "none"])
        
        # use a table constraint because I don't want to expend the brain power to write a new constraint class for this
        # for each plane i, create a constraint over the pairs of flights to see if they are feasible
        # insert each pair of flights into a table constraint
        for i in range(len(var_array)):
            for j in range(len(var_array[i]) - 1):
                departure = var_array[i][j]
                arrival = var_array[i][j + 1]

                cnstr_3 = TableConstraint(name="C3_plane_{}_departure_{}_arrival_{}".format(planes[i], departure, arrival), \
                                        scope=[departure, arrival], satisfyingAssignments=valid_connections)
                constraint_list.extend([cnstr_3])

        # C4: all planes must be serviced within a certain minimum frequency
        required_values = []

        # if number of flights flown by that plane is less than min_maintenance_frequency, then it doesn't need any maintenance
        required_values.append("none")

        # add the maintenance flights
        """ for flight in maintenance_flights:
            required_values.append(flight) """
        required_values.extend(maintenance_flights)

        # for each plane i, use a sliding window with width min_maintenance_frequency to check if the flights within that window satisfy the constraint
        for i in range(len(var_array)):
            for j in range(len(var_array[i]) - min_maintenance_frequency + 1):
                sliding_window = var_array[i][j : j + min_maintenance_frequency]

                # MaintenanceConstraint.__init__(scope, min_maintenance_frequency, maintenance_flights)
                cnstr_4 = MaintenanceConstraint(name='C4_plane_{}_sliding_window_{}_{}'.format(planes[i], j, j + min_maintenance_frequency), \
                                                scope=sliding_window, min_maintenance_frequency = min_maintenance_frequency, \
                                                maintenance_flights = maintenance_flights, plane_can_fly=can_fly[planes[i]])
                constraint_list.extend([cnstr_4])

        # C5: each flight must be scheduled and 
        # C6: no flight can be scheduled more than once
        vars = [var for row in var_array for var in row]
        
        cnstr_5_6 = EachFlightScheduledOnceConstraint(name="C5_C6", scope=vars, all_flights=flights)
        
        constraint_list.extend([cnstr_5_6])

        csp = CSP("PlaneScheduling", vars, constraint_list)
        return csp

    csp = plane_csp(planes_problem)

    #invoke search with the passed parameters
    solutions, num_nodes = bt_search(algo, csp, variableHeuristic, allsolns, trace) 

    all_solutions = []

    if not silent:
        print("Explored {} nodes".format(num_nodes))

    if len(solutions) == 0:
        if not silent:
            print("No solutions to {} found".format(csp.name()))
    else:
        for solution in solutions:
            #Convert each solution into a list of lists specifying a schedule
            #for each plane in the format described above.
            a_solution = []
            sol_dict = dict() # desired format: {plane_name: (flight_position, flight_name), (flight_position, flight_name), ...}
            
            for (var, value) in solution:
                name = var.name() # will be in format: "Plane AC-number Flight number number"
                name = name.split(" ") # will be in format ['Plane', AC-##, 'Flight', 'number', #]
                plane_name = name[1] # retrieve the plane's name (ie: AC-number)
                flight_position = name[-1] # retrieve the flight's position (ie: number)
                # value is the flght itself (ie: AC001, AC002, etc.)

                if plane_name not in sol_dict:
                    sol_dict[plane_name] = []
                    sol_dict[plane_name].append([flight_position, value])
                else:
                    sol_dict[plane_name].append([flight_position, value])
            
            # order a_solution by increasing plane name
            plane_names = list(sol_dict.keys())
            plane_names.sort()

            for name in plane_names:
                sol_list = []
                sol_list.append(name)

                flight_info = sol_dict[name] # will be in format (flight_position, flight_name)

                for entry in flight_info:
                    flight = entry[1] # retrieve the flight name

                    if flight != "none":
                        sol_list.append(flight)
                        
                a_solution.append(sol_list)

            #then return a list containing all converted solutions
            #(i.e., a list of lists of lists)
            all_solutions.append(a_solution)
        
    return all_solutions