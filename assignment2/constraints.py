from csp import Constraint, Variable
import util
from collections import Counter

class TableConstraint(Constraint):
    '''General type of constraint that can be use to implement any type of
       constraint. But might require a lot of space to do so.

       A table constraint explicitly stores the set of satisfying
       tuples of assignments.'''

    def __init__(self, name, scope, satisfyingAssignments):
        '''Init by specifying a name and a set variables the constraint is over.
           Along with a list of satisfying assignments.
           Each satisfying assignment is itself a list, of length equal to
           the number of variables in the constraints scope.
           If sa is a single satisfying assignment, e.g, sa=satisfyingAssignments[0]
           then sa[i] is the value that will be assigned to the variable scope[i].


           Example, say you want to specify a constraint alldiff(A,B,C,D) for
           three variables A, B, C each with domain [1,2,3,4]
           Then you would create this constraint using the call
           c = TableConstraint('example', [A,B,C,D],
                               [[1, 2, 3, 4], [1, 2, 4, 3], [1, 3, 2, 4],
                                [1, 3, 4, 2], [1, 4, 2, 3], [1, 4, 3, 2],
                                [2, 1, 3, 4], [2, 1, 4, 3], [2, 3, 1, 4],
                                [2, 3, 4, 1], [2, 4, 1, 3], [2, 4, 3, 1],
                                [3, 1, 2, 4], [3, 1, 4, 2], [3, 2, 1, 4],
                                [3, 2, 4, 1], [3, 4, 1, 2], [3, 4, 2, 1],
                                [4, 1, 2, 3], [4, 1, 3, 2], [4, 2, 1, 3],
                                [4, 2, 3, 1], [4, 3, 1, 2], [4, 3, 2, 1]])
          as these are the only assignments to A,B,C respectively that
          satisfy alldiff(A,B,C,D)
        '''

        Constraint.__init__(self,name, scope)
        self._name = "TableCnstr_" + name
        self.satAssignments = satisfyingAssignments

    def check(self):
        '''check if current variable assignments are in the satisfying set'''
        assignments = []
        for v in self.scope():
            if v.isAssigned():
                assignments.append(v.getValue())
            else:
                return True
        return assignments in self.satAssignments

    def hasSupport(self, var,val):
        '''check if var=val has an extension to an assignment of all variables in
           constraint's scope that satisfies the constraint. Important only to
           examine values in the variable's current domain as possible extensions'''
        if var not in self.scope():
            return True   #var=val has support on any constraint it does not participate in
        vindex = self.scope().index(var)
        found = False
        for assignment in self.satAssignments:
            if assignment[vindex] != val:
                continue   #this assignment can't work it doesn't make var=val
            found = True   #Otherwise it has potential. Assume found until shown otherwise
            for i, v in enumerate(self.scope()):
                if i != vindex and not v.inCurDomain(assignment[i]):
                    found = False  #Bummer...this assignment didn't work it assigns
                    break          #a value to v that is not in v's curDomain
                                   #note we skip checking if val in in var's curDomain
            if found:     #if found still true the assigment worked. We can stop
                break
        return found     #either way found has the right truth value


class QueensConstraint(Constraint):
    '''Queens constraint between queen in row i and row j'''
    def __init__(self, name, qi, qj, i, j):
        scope = [qi, qj]
        Constraint.__init__(self,name, scope)
        self._name = "QueenCnstr_" + name
        self.i = i
        self.j = j

    def check(self):
        qi = self.scope()[0]
        qj = self.scope()[1]
        if not qi.isAssigned() or not qj.isAssigned():
            return True
        return self.queensCheck(qi.getValue(),qj.getValue())

    def queensCheck(self, vali, valj):
        diag = abs(vali - valj) == abs(self.i - self.j)
        return not diag and vali != valj

    def hasSupport(self, var, val):
        '''check if var=val has an extension to an assignment of the
           other variable in the constraint that satisfies the constraint'''
        #hasSupport for this constraint is easier as we only have one
        #other variable in the constraint.
        if var not in self.scope():
            return True   #var=val has support on any constraint it does not participate in
        otherVar = self.scope()[0]
        if otherVar == var:
            otherVar = self.scope()[1]
        for otherVal in otherVar.curDomain():
            if self.queensCheck(val, otherVal):
                return True
        return False

class QueensTableConstraint(TableConstraint):
    '''Queens constraint between queen in row i and row j, but
       using a table constraint instead. That is, you
       have to create and add the satisfying tuples.

       Since we inherit from TableConstraint, we can
       call TableConstraint.__init__(self,...)
       to set up the constraint.

       Then we get hasSupport and check automatically from
       TableConstraint
    '''
    #your implementation for Question 1 goes
    #inside of this class body. You must not change
    #the existing function signatures.
    def __init__(self, name, qi, qj, i, j):
        self._name = "Queen_" + name
        #util.raiseNotDefined()
        scope = [qi, qj]
        #TableConstraint.__init__(self, name, scope, satisfyingAssignments)
        satisfying_assignments = self.satisfyingAssignments(qi, qj, i, j)
        TableConstraint.__init__(self, name=name, scope=scope, satisfyingAssignments=satisfying_assignments)

    # NQueens constraint: 2 queens cannot be on the same row, same column, or the same diagonal
    # same row: i != j, already guaranteed by the problem setup so we don't need to check this
    # same column: Qi != Qj for all i != j
    # same diagonal: abs(Qi - Qj) != abs(i - j)
    def satisfyingAssignments(self, qi, qj, i, j):
        satisfying_assignments = []

        for qi_col in qi.domain():
            for qj_col in qj.domain():
                # check column constraint
                    if qi_col != qj_col:
                        # check diagonal constraint
                        if abs(qi_col - qj_col) != abs(i - j):
                            satisfying_assignments.append([qi_col, qj_col]) 
        
        return satisfying_assignments

class NeqConstraint(Constraint):
    '''Neq constraint between two variables'''
    def __init__(self, name, scope):
        if len(scope) != 2:
            print("Error Neq Constraints are only between two variables")
        Constraint.__init__(self,name, scope)
        self._name = "NeqCnstr_" + name

    def check(self):
        v0 = self.scope()[0]
        v1 = self.scope()[1]
        if not v0.isAssigned() or not v1.isAssigned():
            return True
        return v0.getValue() != v1.getValue()

    def hasSupport(self, var, val):
        '''check if var=val has an extension to an assignment of the
           other variable in the constraint that satisfies the constraint'''
        #hasSupport for this constraint is easier as we only have one
        #other variable in the constraint.
        if var not in self.scope():
            return True   #var=val has support on any constraint it does not participate in
        otherVar = self.scope()[0]
        if otherVar == var:
            otherVar = self.scope()[1]
        for otherVal in otherVar.curDomain():
            if val != otherVal:
                return True
        return False

class AllDiffConstraint(Constraint):
    '''All diff constraint between a set of variables
       If you are curious as to how to more efficiently perform GAC on
       an AllDiff see
       http://www.constraint-programming.com/people/regin/papers/alldiff.pdf'''
    def __init__(self, name, scope):
        Constraint.__init__(self,name, scope)
        self._name = "AllDiff_" + name

    def check(self):
        assignments = []
        for v in self.scope():
            if v.isAssigned():
                assignments.append(v.getValue())
            else:
                return True
        return len(set(assignments)) == len(assignments)

    def hasSupport(self, var, val):
        '''check if var=val has an extension to an assignment of the
           other variable in the constraint that satisfies the constraint'''
        if var not in self.scope():
            return True   #var=val has support on any constraint it does not participate in

        #since the contraint has many variables use the helper function 'findvals'
        #for that we need two test functions
        #1. for testing complete assignments to the constraint's scope
        #   return True if and only if the complete assignment satisfies the constraint
        #2. for testing partial assignments to see if they could possibly work.
        #   return False if the partial assignment cannot be extended to a satisfying complete
        #   assignment
        #
        #Function #2 is only needed for efficiency (sometimes don't have one)
        #  if it isn't supplied findvals will use a function that never returns False
        #
        #For alldiff, we do have both functions! And they are the same!
        #We just check if the assignments are all to different values. If not return False
        def valsNotEqual(l):
            '''tests a list of assignments which are pairs (var,val)
               to see if they can satisfy the all diff'''
            vals = [val for (var, val) in l]
            return len(set(vals)) == len(vals)
        varsToAssign = self.scope()
        varsToAssign.remove(var)
        x = findvals(varsToAssign, [(var, val)], valsNotEqual, valsNotEqual)
        return x


def findvals(remainingVars, assignment, finalTestfn, partialTestfn=lambda x: True):
    '''Helper function for finding an assignment to the variables of a constraint
       that together with var=val satisfy the constraint. That is, this
       function looks for a supporing tuple.

       findvals uses recursion to build up a complete assignment, one value
       from every variable's current domain, along with var=val.

       It tries all ways of constructing such an assignment (using
       a recursive depth-first search).

       If partialTestfn is supplied, it will use this function to test
       all partial assignments---if the function returns False
       it will terminate trying to grow that assignment.

       It will test all full assignments to "allVars" using finalTestfn
       returning once it finds a full assignment that passes this test.

       returns True if it finds a suitable full assignment, False if none
       exist. (yes we are using an algorithm that is exactly like backtracking!)'''

    # print("==>findvars([",)
    # for v in remainingVars: print(v.name(), " ", end='')
    # print("], [",)
    # for x,y in assignment: print("({}={}) ".format(x.name(),y), end='')
    # print("")

    #sort the variables call the internal version with the variables sorted
    remainingVars.sort(reverse=True, key=lambda v: v.curDomainSize())
    return findvals_(remainingVars, assignment, finalTestfn, partialTestfn)

def findvals_(remainingVars, assignment, finalTestfn, partialTestfn):
    '''findvals_ internal function with remainingVars sorted by the size of
       their current domain'''
    if len(remainingVars) == 0:
        return finalTestfn(assignment)
    var = remainingVars.pop()
    for val in var.curDomain():
        assignment.append((var, val))
        if partialTestfn(assignment):
            if findvals_(remainingVars, assignment, finalTestfn, partialTestfn):
                return True
        assignment.pop()   #(var,val) didn't work since we didn't do the return
    remainingVars.append(var)
    return False


class NValuesConstraint(Constraint):
    '''NValues constraint over a set of variables.  Among the variables in
       the constraint's scope the number that have been assigned
       values in the set 'required_values' is in the range
       [lower_bound, upper_bound] (lower_bound <= #of variables
       assigned 'required_value' <= upper_bound)

       For example, if we have 4 variables V1, V2, V3, V4, each with
       domain [1, 2, 3, 4], then the call
       NValuesConstraint('test_nvalues', [V1, V2, V3, V4], [3,2], 2,
       3) will only be satisfied by assignments such that at least 2
       the V1, V2, V3, V4 are assigned the value 3 or 2, and at most 3
       of them have been assigned the value 3 or 2.

    '''

    def __init__(self, name, scope, required_values, lower_bound, upper_bound):
        Constraint.__init__(self,name, scope)
        self._name = "NValues_" + name
        self._required = required_values
        self._lb = lower_bound
        self._ub = upper_bound

    def check(self):
        #util.raiseNotDefined()

        if self.numUnassigned() > 0:
            return True
        
        num_occurrences = 0

        for v in self.scope():
            if v.getValue() in self._required:
                num_occurrences += 1

        if num_occurrences >= self._lb and num_occurrences <= self._ub:
            return True
        else:
            return False

    def hasSupport(self, var, val):
        '''check if var=val has an extension to an assignment of the
           other variable in the constraint that satisfies the constraint

           HINT: check the implementation of AllDiffConstraint.hasSupport
                 a similar approach is applicable here (but of course
                 there are other ways as well)
        '''
        #util.raiseNotDefined()
        if var not in self.scope():
            return True # var=val has support on any constraint it does not participate in

        # check if bounds are satisfied
        def bounds_satisfied(l):
            num_occurrences = 0

            for (variable, value) in l:
                if value in self._required:
                    num_occurrences += 1
            
            if num_occurrences >= self._lb and num_occurrences <= self._ub:
                return True
            else:
                return False

        # check if lower bound is satisfied
        def lower_bound_satisfied(l):
            num_occurrences = 0

            for (variable, value) in l:
                if value in self._required:
                    num_occurrences += 1
            
            if num_occurrences >= self._lb and num_occurrences <= self._ub:
                return True
            else:
                return False

        # check if upper bound is satisfied
        def upper_bound_satisfied(l):
            num_occurrences = 0

            for (variable, value) in l:
                if value in self._required:
                    num_occurrences += 1
            
            if num_occurrences <= self._ub:
                return True
            else:
                return False
        
        varsToAssign = self.scope()
        varsToAssign.remove(var)

        x = findvals(varsToAssign, [(var, val)], lower_bound_satisfied, upper_bound_satisfied)
        #x = findvals(varsToAssign, [(var, val)], bounds_satisfied)

        return x

# plane_scheduling.py constraints
class MaintenanceConstraint(Constraint):
    #def __init__(self, name, scope, flown_flights, all_flights):
    def __init__(self, name, scope, min_maintenance_frequency, maintenance_flights, plane_can_fly):
        Constraint.__init__(self, name, scope)
        self._name = 'Maintenance_' + name
        self._scope = scope # a range of min_maintenance_frequency flights
        self.min_maintenance_frequency = min_maintenance_frequency
        self.maintenance_flights = maintenance_flights
        self._plane_can_fly= plane_can_fly

    def check(self):
        # v = variable = plane (ex: AC-1)
        num_non_maintenance_flights = 0

        # constraint check that's mostly meant to solve P9 in time
        # check if the maintenance flights can be flown by a plane
        non_flyable_maintenance_flights = 0
        for flight in self.maintenance_flights:
            if flight not in self._plane_can_fly:
                non_flyable_maintenance_flights += 1
        
        # if there is at least 1 maintenance flight that can be flown by a plane, continue with the rest of the constraint check
        # otherwise, if no maintenance flight can be flown by a plane, return False
        if non_flyable_maintenance_flights == len(self.maintenance_flights):
            return False

        for v in self.scope():
            if v.isAssigned():
                value = v.getValue()
                
                # last flight in a sequence
                # if we didn't return yet, then the sequence is valid wrt. the maintenance frequency
                # so return True
                if value == "none":
                    return True

                # haven't encountered a maintenance depot, increment the counter
                if value not in self.maintenance_flights:
                    num_non_maintenance_flights += 1
                else:
                    # reset the counter if we encounter a maintenance depot
                    num_non_maintenance_flights = 0

                if num_non_maintenance_flights >= self.min_maintenance_frequency:
                    return False
            else:
                return True
        
        return True

    def hasSupport(self, var, val):
        '''check if var=val has an extension to an assignment of the
           other variable in the constraint that satisfies the constraint'''

        if var not in self.scope():
            return True # var=val has support on any constraint it does not participate in

        def check_full_assignment(l):
            num_non_maintenance_flights = 0
            
            # constraint check that's mostly meant to solve P9 in time
            # check if the maintenance flights can be flown by a plane
            non_flyable_maintenance_flights = 0
            for flight in self.maintenance_flights:
                if flight not in self._plane_can_fly:
                    non_flyable_maintenance_flights += 1
            
            # if there is at least 1 maintenance flight that can be flown by a plane, continue with the rest of the constraint check
            # otherwise, if no maintenance flight can be flown by a plane, return False
            if non_flyable_maintenance_flights == len(self.maintenance_flights):
                return False

            for var, value in l:
                # last flight in a sequence
                # if we didn't return yet, then the sequence is valid wrt. the maintenance frequency
                # so return True
                if value == "none":
                    return True
                
                # haven't encountered a maintenance depot, increment the counter
                if value not in self.maintenance_flights:
                    num_non_maintenance_flights += 1
                else:
                    # reset the counter if we encounter a maintenance depot
                    num_non_maintenance_flights = 0

                if num_non_maintenance_flights >= self.min_maintenance_frequency:
                    return False
            
            return True

        varsToAssign = self.scope()
        varsToAssign.remove(var)

        # there is no such thing as a partial assignment since the maintenance needs to be valid over every sliding window
        # so pass partial assignment the same function arg as full assignment
        x = findvals(varsToAssign, [(var, val)], check_full_assignment, check_full_assignment)

        return x

class EachFlightScheduledOnceConstraint(Constraint):
    #def __init__(self, name, scope, flown_flights, all_flights):
    def __init__(self, name, scope, all_flights):
        Constraint.__init__(self, name, scope)
        self._name = 'EachFlightScheduledOnce_' + name
        self._scope = scope # the planes
        self._all_flights = all_flights
        self.total_num_flights = len(set(all_flights))

    def check(self):
        assignments = dict()

        # v = variable = plane (ex: AC-1)
        for v in self.scope():
            if v.isAssigned():
                value = v.getValue()

                # count the number of times a value/flight occurs
                if value != "none":
                    if value in assignments:
                        assignments[value] += 1
                    else:
                        assignments[value] = 1
            else:
                return True

        # not all flights have been flown
        if len(assignments) < self.total_num_flights:
            return False
        
        # a flight has been flown more than once
        for key, val in assignments.items():
            if val > 1:
                return False

        return True

    def hasSupport(self, var, val):
        '''check if var=val has an extension to an assignment of the
           other variable in the constraint that satisfies the constraint'''

        if var not in self.scope():
            return True # var=val has support on any constraint it does not participate in

        # final assignments
        # assignment valid only if the flight hasn't been flown yet
        def check_all_flights_flown(l):
            assignments = dict()

            for (var, value) in l:
                if value != "none":
                    if value in assignments:
                        assignments[value] += 1
                    else:
                        assignments[value] = 1
            
            # not all flights have been flown
            if len(assignments) < self.total_num_flights:
                return False
            
            # a flight has been flown more than once
            for key, val in assignments.items():
                if val > 1:
                    return False

            return True

        def check_some_flights_flown(l):
            assignments = dict()

            for (var, value) in l:
                if value != "none":
                    if value in assignments:
                        assignments[value] += 1
                    else:
                        assignments[value] = 1

            # don't check for whether a flight hasn't been flown because maybe it hasn't been assigned yet

            # a flight has been flown more than once
            for key, val in assignments.items():
                if val > 1:
                    return False

            return True

        varsToAssign = self.scope()
        varsToAssign.remove(var)
        x = findvals(varsToAssign, [(var, val)], check_all_flights_flown, check_some_flights_flown)

        return x
