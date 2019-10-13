#This is an adaptation of aima search code
#Author - Abhisek Banerjee (axb180050@utdallas.edu/banerjee.abhisek1990@gmail.com)
import bisect
import math
import random
import sys
from collections import deque

from utils import (
    is_in, argmin, argmax, argmax_random_tie, probability, weighted_sampler,
    memoize, print_table, open_data, PriorityQueue, name,
    distance, vector_add
)

infinity = float('inf')
city_number_list = dict()
number_to_city_map = dict()
heuristic_map = dict()
def trace_path(goal):
    print("Reached goal state")
    print("Path to the goal from the initial state")
    path = list()
    node = goal
    while node.parent != None:
        path.append(node)
        node = node.parent
    path.append(node)
    while path:
        print(number_to_city_map[path.pop().state])
    print("-----------------------\n")


# ______________________________________________________________________________
# ______________________________________________________________________________

class Problem(object):

    initial = 0  
    goal= 0
    problem_graph = list()
    node_count = 0 
    def __init__(self, graph, initial, goal, nodes):
        self.initial = initial
        self.goal = goal
        self.problem_graph = graph.copy()
        self.node_count = nodes

    def actions(self, state):
        child_nodes = list()
        for i in range(self.node_count):
            if self.problem_graph[state][i] > 0:
                child_nodes.append(i)
        return child_nodes


    def result(self, state, action):
        return action

    def goal_test(self, state):
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        return c + self.problem_graph[state1][state2]

    def value(self, state):
        raise NotImplementedError


# ______________________________________________________________________________


class Node:

    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1
    def __repr__(self):
        return number_to_city_map[self.state] 
    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action,
                         problem.path_cost(self.path_cost, self.state,
                                           action, next_state))
        return next_node

    def solution(self):
        return [node.action for node in self.path()[1:]]

    def path(self):
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))


    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash(self.state)


# ______________________________________________________________________________


def best_first_graph_search(problem, f):

    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)

    explored = list()
    itr = 1
    print("Initial Node: "+number_to_city_map[node.state])
    while frontier:
        print("Iteration#"+str(itr))
        dist, current_city = frontier.heap[0]
        print("Current Node: "+number_to_city_map[current_city.state])
        itr = itr+1
        node = frontier.pop()
        if problem.goal_test(node.state):
            print ("Found the goal node")
            print(trace_path(node))
            return node
        print("Evaluation function("+number_to_city_map[current_city.state]+")"+"="+str(dist))
        explored.append(node.state)
        print("Explored:")
        explrd = list()
        for e in explored:
            explrd.append(number_to_city_map[e])
        print(explrd)

        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
        frnt = dict()
        print("Frontier:")
        for e in frontier.heap:
            dist, city = e
            frnt[city] = dist
        print(sorted(frnt.items(), key=lambda x: x[1]))

    return None


def astar_search(problem, h=None):

    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))


def recursive_best_first_search(problem, h=None):

    h = memoize(h or problem.h, 'h')

    def RBFS(problem, node, flimit):
        if problem.goal_test(node.state):
            print("Reached Dallas, which is the destination city")
            return node, 0  # (The second value is immaterial)
        successors = node.expand(problem)
        if len(successors) == 0:
            return None, infinity
        for s in successors:
            s.f = max(s.path_cost + h(s), node.f)
        while True:
            # Order by lowest f value
            successors.sort(key=lambda x: x.f)
            best = successors[0]
            if len(successors) > 1:
                alternative = successors[1].f
            else:
                alternative = infinity

            print("f_limit:"+str(flimit))
            print("best:"+str(best.f))
            print("alternative:"+str(alternative))
            print("current_city:"+number_to_city_map[node.state])
            if best.f > flimit:
                print("next_city: Fail")
                print("\n")
                return None, best.f
            print("next_city:"+number_to_city_map[best.state])
            print("\n")
            result, best.f = RBFS(problem, best, min(flimit, alternative))
            if result is not None:
                return result, best.f

    node = Node(problem.initial)
    node.f = h(node)
    result, bestf = RBFS(problem, node, infinity)
    trace_path(result)
    return result

def consistent_heuristic_checker(graph, node_count):
    for i in range(node_count):
        for j in range(node_count):
            if (graph[i][j] > 0):
                print("-----")
                print("Parent city " +number_to_city_map[i] +" with heuristic " + str(heuristic_map[i]))
                print("Child city " +number_to_city_map[j] +" with heuristic " + str(heuristic_map[j]))
                print("Distance between these two cities: "+ str(graph[i][j]))
                if (heuristic_map[i] > (heuristic_map[j] +graph[i][j])):
                    print("This is not consistent")
                    print("-----")
                    return False
                print("-----")
    return True

def heuristic(n):
    return heuristic_map[n.state]

if __name__ == "__main__":
    if (len(sys.argv)) != 5:
        print("Invalid number of arguments.")
        sys.exit()
    heuristic_file = sys.argv[1].strip()
    distance_file = sys.argv[2].strip()
    initial = sys.argv[3].strip()
    goal = sys.argv[4].strip()
    i = 0
    #Read the heuristic file
    with open(heuristic_file) as fp:
        for line in fp:
            city, dist = line.rsplit(' ',1)
            h_dist = int(dist.strip())
            city_number_list[city.strip()] = i
            number_to_city_map[i] = city.strip()
            heuristic_map[i] = h_dist
            i = i+1
    city_number_list[goal] = i
    number_to_city_map[i] = goal
    heuristic_map[i] = 0 
    i = i+1
    distance_graph = list()
    for a in range(i):
        temp = list()
        for b in range(i):
            temp.append(0)
        distance_graph.append(temp)
    #Read the distance graph
    with open(distance_file) as fp:
        for line in fp:
            city_source, second_part = line.split('---')
            city_source = city_source.strip()
            city_dest, dist = second_part.split(':::')
            city_dest = city_dest.strip()
            num_dist = int(dist.strip())
            distance_graph[city_number_list[city_source]][city_number_list[city_dest]]= num_dist
            distance_graph[city_number_list[city_dest]][city_number_list[city_source]]= num_dist

    print("Check consistency of the given heuristic.")
    consistent = consistent_heuristic_checker(distance_graph, i)
    if(consistent):
        print("Heuristic is consistent.")
    else:
         print("Heuristic is not consistent.")
    print("\nA* algorithm\n")
    astar_search(Problem(distance_graph, city_number_list[initial], city_number_list[goal],i),heuristic)
    print("\nRBFS algorithm\n")
    recursive_best_first_search(Problem(distance_graph, city_number_list[initial], city_number_list[goal],i),heuristic)
    print("\n")


