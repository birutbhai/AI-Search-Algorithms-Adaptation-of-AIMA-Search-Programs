#This is an adaptation of the aima search code
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
total_player = 0


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
        print(path.pop().state)
    print("-----------------------\n")


class Problem(object):

    def __init__(self, initial, goal=None):

        self.initial = initial
        self.goal = goal

    def actions(self, state):
        #Compute all valid state from given state
        ans = list()
        if state[4] == 'L':
            if(state[0] >= 2):
                if ((state[1] <= (state[0]-2)) or state[0] == 2) and (state[3] <= (state[2]+2)):
                    ans.append([state[0] - 2, state[1], state[2]+2, state[3], 'R'])
            if(state[0] >= 1):
                if ((state[1] <= (state[0]-1)) or state[0] == 1) and (state[3] <= (state[2]+1)):
                    ans.append([state[0] - 1, state[1], state[2]+1, state[3], 'R'])
            if(state[1] >= 2):
                if ((state[2] >= (state[3] +2)) or state[2] == 0):
                    ans.append([state[0], state[1]-2, state[2], state[3]+2, 'R'])
            if(state[1] >= 1):
                if (state[2] >= (state[3] +1)) or state[2] == 0:
                    ans.append([state[0], state[1]-1, state[2], state[3]+1, 'R'])
            if((state[0] >= 1 and state[1] >= 1)) and ((state[3]+1) <= (state[2]+1)):
                ans.append([state[0]-1, state[1]-1, state[2]+1, state[3]+1, 'R'])
        else:
            if(state[2] >= 2):
                if (state[3] <= (state[2]-2) or state[2] == 2) and (state[1] <= (state[0]+2)):
                    ans.append([state[0] + 2, state[1], state[2]-2, state[3], 'L'])
            if(state[2] >= 1):
                if (state[3] <= (state[2]-1) or state[2] == 1) and (state[1] <= (state[0]+1)):
                    ans.append([state[0] + 1, state[1], state[2]-1, state[3], 'L'])
            if(state[3] >= 2):
                if state[0] >= (state[1] +2) or state[0] == 0:
                    ans.append([state[0], state[1]+2, state[2], state[3]-2, 'L'])
            if(state[3] >= 1):
                if state[0] >= (state[1] +1) or state[0] == 0:
                    ans.append([state[0], state[1]+1, state[2], state[3]-1, 'L'])
            if(state[2] >= 1 and state[3] >= 1) and ((state[0]+1) <= (state[1]+1)):
                ans.append([state[0]+1, state[1]+1, state[2]-1, state[3]-1, 'L'])

        return ans



    def result(self, state, action):

        return action

    def goal_test(self, state):

        if isinstance(self.goal, list):
            return state == self.goal

    def path_cost(self, c, state1, action, state2):

        return c + 1

    def value(self, state):

        raise NotImplementedError


# ______________________________________________________________________________


class Node:

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
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
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))


    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash(self.state)



def best_first_graph_search(problem, f):

    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = list()
    while frontier:
        node = frontier.pop()
        print("Current Node:", node.state)
        if problem.goal_test(node.state):
            trace_path(node)
            return node
        explored.append(node.state)
        print("Explored Nodes:", explored)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
        temp_front = list()
        for e in frontier.heap:
            val, node = e
            temp_front.append(node.state)
        print("Frontier Nodes:", temp_front)
        print("\n")
    return None


def uniform_cost_search(problem):
    return best_first_graph_search(problem, lambda node: node.path_cost)


def depth_limited_search(problem, limit=50):

    def recursive_dls(node, problem, limit):
        if problem.goal_test(node.state):
            trace_path(node)
            return node
        elif limit == 0:
            return 'cutoff'
        else:
            cutoff_occurred = False
            for child in node.expand(problem):
                result = recursive_dls(child, problem, limit - 1)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result
            return 'cutoff' if cutoff_occurred else None

    # Body of depth_limited_search:
    return recursive_dls(Node(problem.initial), problem, limit)


def iterative_deepening_search(problem):
    for depth in range(sys.maxsize):
        result = depth_limited_search(problem, depth)
        if result != 'cutoff':
            return result



def heuristic(n):
        # Elements at the L side - 1
        return (n.state[0]+n.state[1]-1)

def greedy_best_first_graph_search(problem, h=None):
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: h(n))




def astar_search(problem, h=None):
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))


def recursive_best_first_search(problem, h=None):
    h = memoize(h or problem.h, 'h')

    def RBFS(problem, node, flimit):
        if problem.goal_test(node.state):
            trace_path(node)
            return node, 0  # (The second value is immaterial)
        successors = node.expand(problem)
        if len(successors) == 0:
            return None, infinity
        for s in successors:
            s.f = max(s.path_cost + h(s), node.f)
        while True:
            # Order by lowest f value
            successors.sort(key=lambda x: x.f)
            alternative = 0
            if len(successors) > 1:
                alternative = successors[1].f
            else:
                alternative = infinity
            best = successors[0]
            print("f_limit:"+str(flimit))
            print("best:"+str(best.f))
            print("alternative:"+str(alternative))
            print("current_city:", node.state)

            if best.f > flimit:
                print("next_city:Fail")
                print("\n")
                return None, best.f
            print("next_city:",best.state)
            print("\n")
            result, best.f = RBFS(problem, best, min(flimit, alternative))
            if result is not None:
                return result, best.f

    node = Node(problem.initial)
    node.f = h(node)
    result, bestf = RBFS(problem, node, infinity)
    return result


if __name__ == "__main__":
    if (len(sys.argv)) != 3:
        print("Invalid number of arguments.")
        sys.exit()
    missionary_count = int(sys.argv[1].strip())
    cannibal_count = int(sys.argv[2].strip())
    if missionary_count < cannibal_count:
        print("Initial state has more cannibals than missionaries. Game over.")
        sys.exit()
    total_player = missionary_count + cannibal_count
    print("Uniform cost search:")

    # Each state looks like a list of 5 attributes [missionary count on the initial side, cannibal count on the initial side,
    # missionary count on the goal side, cannibal count on the goal side, current boat location]. Boat location could be either L 
    # or initial side, or R or the goal side. During state transition the boat has to move to the other side and cannibal count at any 
    # side can never be more than the missionary count.

    uniform_cost_search(Problem([missionary_count,cannibal_count, 0, 0, 'L'], [0,0, missionary_count,cannibal_count,'R']))
    print("Iterative deepening search:")
    iterative_deepening_search(Problem([missionary_count,cannibal_count, 0, 0, 'L'], [0,0, missionary_count,cannibal_count,'R']))
    print("Greedy best first search:")
    greedy_best_first_graph_search(Problem([missionary_count,cannibal_count, 0, 0, 'L'], [0,0, missionary_count,cannibal_count,'R']), heuristic)
    print("A*:")
    astar_search(Problem([missionary_count,cannibal_count, 0, 0, 'L'], [0,0, missionary_count,cannibal_count,'R']), heuristic)
    print("RBFS:")
    recursive_best_first_search(Problem([missionary_count,cannibal_count, 0, 0, 'L'], [0,0, missionary_count,cannibal_count,'R']), heuristic)

