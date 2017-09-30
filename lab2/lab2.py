# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
    to_visit = [ [start] ]
    
    while len(to_visit) > 0:
        f = to_visit[0]
        to_visit = to_visit[1:]
        curr_node = f[-1]

        if curr_node == goal:
            return f
        
        connected_nodes = graph.get_connected_nodes(curr_node)
        # print ('{} -> {}', curr_node, connected_nodes)
        for N in connected_nodes:
            if N in f:
                continue
            temp = list(f)
            temp.append(N)
            to_visit.append(temp)

    return None

## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
    to_visit = [ [start] ]
    
    while len(to_visit) > 0:
        f = to_visit[0]
        curr_node = f[-1]

        if curr_node == goal:
            break
        
        to_visit = to_visit[1:]
        
        connected_nodes = graph.get_connected_nodes(curr_node)
        for N in connected_nodes:
            if N in f:
                continue
            temp = list(f)
            temp.append(N)
            to_visit = [temp] + to_visit

    if len(to_visit) == 0:
        return None

    return f

import heapq

## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
    to_visit = [ (graph.get_heuristic(start, goal), [start]) ]
   
    while len(to_visit) > 0:
        f = to_visit[0][1]
        to_visit = to_visit[1:]

        curr_node = f[-1]

        if curr_node == goal:
            return f

        connected_nodes = graph.get_connected_nodes(curr_node)
        # print ('{} -> {}'.format(curr_node, [(N, graph.get_heuristic(N, goal)) for N in connected_nodes]))
        valid_paths = []
        for N in connected_nodes:
            if N in f: # Would create path cycle
                continue
            temp = list(f)
            temp.append(N)

            valid_paths.append((graph.get_heuristic(N, goal), temp))
        
        to_visit = sorted(valid_paths) + to_visit

    return None

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    to_visit = [ (graph.get_heuristic(start, goal), [start] ) ]
    
    while len(to_visit) > 0:
        next_nodes = []

        for _,f in to_visit:
            curr_node = f[-1] 

            if curr_node == goal:
                return f
            
            connected_nodes = graph.get_connected_nodes(curr_node)
            # print ('{} -> {}'.format(curr_node, [(N, graph.get_heuristic(N, goal)) for N in connected_nodes]))
            
            for N in connected_nodes:
                if N in f:
                    continue
                temp = list(f)
                temp.append(N)
        
                next_nodes.append((graph.get_heuristic(N, goal), temp))

        to_visit = sorted(next_nodes)[:beam_width]

    return []

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.


## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    L = 0
    for A,B in zip(node_names[:-1], node_names[1:]):
        edge = graph.get_edge(A,B)
        L += edge.length

    return L


def branch_and_bound(graph, start, goal):
    to_visit = [ (0, [start]) ]
   
    while len(to_visit) > 0:
        distance = to_visit[0][0]
        f = heapq.heappop(to_visit)[1]

        curr_node = f[-1]

        if curr_node == goal:
            return f

        connected_nodes = graph.get_connected_nodes(curr_node)
        # print ('{} -> {}'.format(curr_node, [(N, graph.get_heuristic(N, goal)) for N in connected_nodes]))
        
        for N in connected_nodes:
            if N in f: # Would create path cycle
                continue
            temp = list(f)
            temp.append(N)

            edge_length = graph.get_edge(curr_node, N).length

            heapq.heappush(to_visit, (distance + edge_length, temp))

    return None
    
def a_star(graph, start, goal):
    to_visit = [ ( graph.get_heuristic(start, goal), [start]) ]
    distance_from_start = {start: 0}

    while len(to_visit) > 0:
        # print(to_visit)
        f = heapq.heappop(to_visit)[1]
        
        curr_node = f[-1]

        if curr_node == goal:
            return f

        connected_nodes = graph.get_connected_nodes(curr_node)
        # print ('{} -> {}'.format(curr_node, [(N, graph.get_edge(curr_node, N).length,graph.get_heuristic(N, goal)) for N in connected_nodes]))
        
        for N in connected_nodes:
            if N in f: # Path cycle
                continue

            # If if our path to N is longer than a previously found path to N, chuck it
            distance = distance_from_start[curr_node] + graph.get_edge(curr_node, N).length
            # if N in distance_from_start and distance >= distance_from_start[N]:
            # Test 39 actually fails if we use the above condition even though it seems better
            if N in distance_from_start:
            
                continue

            temp = list(f)
            temp.append(N)

            heapq.heappush(to_visit, (distance + graph.get_heuristic(N, goal), temp))
            distance_from_start[N] = distance

    return []

## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    raise NotImplementedError

def is_consistent(graph, goal):
    raise NotImplementedError

HOW_MANY_HOURS_THIS_PSET_TOOK = ''
WHAT_I_FOUND_INTERESTING = ''
WHAT_I_FOUND_BORING = ''
