# MIT 6.034 Lab 4: Constraint Satisfaction Problems
# Written by 6.034 staff

from constraint_api import *
from test_problems import get_pokemon_problem


#### Part 1: Warmup ############################################################

def has_empty_domains(csp) :
    """Returns True if the problem has one or more empty domains, otherwise False"""
    # Pep8: For sequences, (strings, lists, tuples), use the fact that empty sequences are false.
    return any(not csp.domains[k] for k in csp.domains)
    
def check_all_constraints(csp) :
    """Return False if the problem's assigned values violate some constraint,
    otherwise True"""
    # print(csp)
    for constraint in csp.constraints:
        if constraint.var1 in csp.assignments and constraint.var2 in csp.assignments:
            if not constraint.constraint_fn(csp.assignments[constraint.var1], csp.assignments[constraint.var2]):
                # Constraint violated
                return False
    return True


#### Part 2: Depth-First Constraint Solver #####################################

def solve_constraint_dfs(problem) :
    """
    Solves the problem using depth-first search.  Returns a tuple containing:
    1. the solution (a dictionary mapping variables to assigned values)
    2. the number of extensions made (the number of problems popped off the agenda).
    If no solution was found, return None as the first element of the tuple.
    """
    # print ('---PROBLEM---')
    # print (problem)

    extensions = 0
    
    # I guess the agenda is the queue?
    agenda = [problem]

    while agenda:
        curr_problem = agenda[0]
        extensions += 1

        # print ('---CURR_PROBLEM---')
        # print (curr_problem)

        if has_empty_domains(curr_problem) or not check_all_constraints(curr_problem):
            agenda = agenda[1:]
            continue

        if not curr_problem.unassigned_vars:
            break

        curr_var = curr_problem.pop_next_unassigned_var()

        append_to_front = []
        for value in curr_problem.get_domain(curr_var):
            new_problem = curr_problem.copy()
            new_problem.set_assignment(curr_var, value)
            append_to_front.append(new_problem)

        agenda = append_to_front + agenda[1:]

    if agenda:
        return (agenda[0].assignments, extensions)
    else:
        return (None, extensions)

# QUESTION 1: How many extensions does it take to solve the Pokemon problem
#    with DFS?

# Hint: Use get_pokemon_problem() to get a new copy of the Pokemon problem
#    each time you want to solve it with a different search method.

ANSWER_1 = solve_constraint_dfs(get_pokemon_problem())[1]


#### Part 3: Forward Checking ##################################################

def eliminate_from_neighbors(csp, var):
    """
    Eliminates incompatible values from var's neighbors' domains, modifying
    the original csp.  Returns an alphabetically sorted list of the neighboring
    variables whose domains were reduced, with each variable appearing at most
    once.  If no domains were reduced, returns empty list.
    If a domain is reduced to size 0, quits immediately and returns None.
    """
    print ('Var: {}'.format(var))
    print ('Domain: {}'.format(csp.get_domain(var)))
    print (csp)

    # We need to group constraints together for Test 22
    constraints = {}
    for constraint in csp.get_all_constraints():
        key = (constraint.var1, constraint.var2)

        if not key in constraints:
            constraints[key] = [constraint]
        else:
            constraints[key].append(constraint)

    # The list of values whose domains were recuduced by this function.
    reduced_domains = []

    for neighbor in csp.get_neighbors(var):
        # print ('Neighbor {}'.format(neighbor))
        orig_domain = csp.get_domain(neighbor)

        if var < neighbor:
            key = (var, neighbor)
            test = lambda var, neighbor: all(C.check(var, neighbor) for C in constraints[key])
        else:
            key = (neighbor, var)
            test = lambda var, neighbor: all(C.check(neighbor, var) for C in constraints[key])

        if key in constraints:
            new_domain = [domain_val for domain_val in orig_domain if any(test(assigned_val, domain_val) for assigned_val in csp.get_domain(var))]
        else:
            new_domain = orig_domain

        # print ('new_domain: {}'.format(new_domain))
        # print ('orig_domain: {}'.format(orig_domain))
        if new_domain != orig_domain:
            if not new_domain:
                # Return None if any domain is reduced to nothing
                csp.set_domain(neighbor, [])
                return None

            reduced_domains.append(neighbor)

            if len(new_domain) == 1:
                csp.set_assignment(neighbor, new_domain[0])
            else:
                csp.set_domain(neighbor, new_domain)

    print('---RESULT---')
    print(csp)
    return reduced_domains

# Because names give us power over things (you're free to use this alias)
forward_check = eliminate_from_neighbors

def solve_constraint_forward_checking(problem) :
    """
    Solves the problem using depth-first search with forward checking.
    Same return type as solve_constraint_dfs.
    """
    print ('Problem: {}'.format(problem))

    extensions= 0

    agenda = [problem]

    while agenda:
        curr_problem = agenda[0]
        extensions += 1

        print ('{}. Considering: {}'.format(extensions, curr_problem.domains))

        if extensions == 9 or extensions == 10:
            print (curr_problem)

        if has_empty_domains(curr_problem) or not check_all_constraints(curr_problem):
            agenda = agenda[1:]
            continue

        if not curr_problem.unassigned_vars:
            break

        curr_var = curr_problem.pop_next_unassigned_var()

        append_to_front = []
        for value in curr_problem.get_domain(curr_var):
            new_problem = curr_problem.copy()
            new_problem.set_assignment(curr_var, value)
            
            eliminate_from_neighbors(new_problem, curr_var)

            append_to_front.append(new_problem)

        agenda = append_to_front + agenda[1:]

    if agenda:
        return (agenda[0].assignments, extensions)
    else:
        return (None, extensions)


# QUESTION 2: How many extensions does it take to solve the Pokemon problem
#    with DFS and forward checking?

ANSWER_2 = None


#### Part 4: Domain Reduction ##################################################

def domain_reduction(csp, queue=None) :
    """
    Uses constraints to reduce domains, propagating the domain reduction
    to all neighbors whose domains are reduced during the process.
    If queue is None, initializes propagation queue by adding all variables in
    their default order. 
    Returns a list of all variables that were dequeued, in the order they
    were removed from the queue.  Variables may appear in the list multiple times.
    If a domain is reduced to size 0, quits immediately and returns None.
    This function modifies the original csp.
    """
    raise NotImplementedError


# QUESTION 3: How many extensions does it take to solve the Pokemon problem
#    with DFS (no forward checking) if you do domain reduction before solving it?

ANSWER_3 = None


def solve_constraint_propagate_reduced_domains(problem) :
    """
    Solves the problem using depth-first search with forward checking and
    propagation through all reduced domains.  Same return type as
    solve_constraint_dfs.
    """
    raise NotImplementedError


# QUESTION 4: How many extensions does it take to solve the Pokemon problem
#    with forward checking and propagation through reduced domains?

ANSWER_4 = None


#### Part 5A: Generic Domain Reduction #########################################

def propagate(enqueue_condition_fn, csp, queue=None) :
    """
    Uses constraints to reduce domains, modifying the original csp.
    Uses enqueue_condition_fn to determine whether to enqueue a variable whose
    domain has been reduced. Same return type as domain_reduction.
    """
    raise NotImplementedError

def condition_domain_reduction(csp, var) :
    """Returns True if var should be enqueued under the all-reduced-domains
    condition, otherwise False"""
    raise NotImplementedError

def condition_singleton(csp, var) :
    """Returns True if var should be enqueued under the singleton-domains
    condition, otherwise False"""
    raise NotImplementedError

def condition_forward_checking(csp, var) :
    """Returns True if var should be enqueued under the forward-checking
    condition, otherwise False"""
    raise NotImplementedError


#### Part 5B: Generic Constraint Solver ########################################

def solve_constraint_generic(problem, enqueue_condition=None) :
    """
    Solves the problem, calling propagate with the specified enqueue
    condition (a function). If enqueue_condition is None, uses DFS only.
    Same return type as solve_constraint_dfs.
    """
    raise NotImplementedError

# QUESTION 5: How many extensions does it take to solve the Pokemon problem
#    with forward checking and propagation through singleton domains? (Don't
#    use domain reduction before solving it.)

ANSWER_5 = None


#### Part 6: Defining Custom Constraints #######################################

def constraint_adjacent(m, n) :
    """Returns True if m and n are adjacent, otherwise False.
    Assume m and n are ints."""
    raise NotImplementedError

def constraint_not_adjacent(m, n) :
    """Returns True if m and n are NOT adjacent, otherwise False.
    Assume m and n are ints."""
    raise NotImplementedError

def all_different(variables) :
    """Returns a list of constraints, with one difference constraint between
    each pair of variables."""
    raise NotImplementedError


#### SURVEY ####################################################################

NAME = None
COLLABORATORS = None
HOW_MANY_HOURS_THIS_LAB_TOOK = None
WHAT_I_FOUND_INTERESTING = None
WHAT_I_FOUND_BORING = None
SUGGESTIONS = None
