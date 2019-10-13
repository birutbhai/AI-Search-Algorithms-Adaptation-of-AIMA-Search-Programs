Abhisek Banerjee - AXB180050@utdallas.edu
CS6364- Homework 1
Files:  ms_ca.py - For Q2. 
        graph_search.py - For Q3. (Two files dest and heu will also be uploaded as example input files.)
Programming language - Python3
Platform - Ubuntu
Aima code: Check out the the AIMA code from,
https://github.com/aimacode/aima-python/blob/master/
Main file used: search.py
Search.py internally uses utils.py. So it is advisable to place the new files in the same directory before running.

Description:
a>ms_ca.py: Performs  (a) uniform-cost search; (b) iterative deepening search; (c) greedy best-first search; (d) A* search and (e) recursive best-first search
for Missionaries and Cannibals Problem.
Input format: python3 ms_ca.py <param1> <paam2> >output_file
All parameters are mandatory. And redirection of output to a file is strongly recommended as the search space can get pretty big, and printing values on STDOUT could take a long time.
Example - python3 ms_ca.py 3 3 >out
param1 - Missionary count.
param - Cannibals count.

This program prints the path to goal and also expanded and frontier lists for all the visited nodes for A*, greedy best-first search and uniform-cost search. For RBFS it prints f_limit, best, alternative, current-city and next-city for each node visited. Each state between path to goal will be in form of a collection of 5 attributes, [missionary count on the initial side, cannibal count on the initial side, missionary count on the goal side, cannibal count on the goal side, current boat location]. Boat location could be either L or initial side, or R or the goal side. During state transition the boat has to move to the other side and cannibal count at any side can never be more than the missionary count.



b> graph_search.py: Performs A* and RBFS search on a given graph with heristic provided as input.
Input format: python3 graph_search.py <param1> <param2> <param3> <param4>
Example - python3 graph_search.py "heu.txt" "dist.txt" "Seattle" "Dallas"

All parameters ar mandatory.
param1: File containing the heuristics in the following format,
Austin 182
Charlotte 929
San Francisco 1230
Los Angeles 1100
.....
It should be provided with in "".


param2: File containing the distance graph in the following format,
Los Angeles --- San Francisco ::: 383
Los Angeles --- Austin ::: 1377
Los Angeles --- Bakersville ::: 153
San Francisco --- Bakersville ::: 283
San Francisco --- Seattle ::: 807
Seattle --- Santa Fe ::: 1463
Seattle --- Chicago ::: 2064
It should be provided with in "".

param3: Name of the initial city.
It should be provided with in "".

param4: Name of the destination city.
It should be provided with in "".


This file first checks if the given heuristic is consistent. Then it performs A* search and RBFS search on the given graph to find out a path between intial city to final city. For A* it prints current node, evaluation function of current node, frontier and the expanded sets for each visited nodes. For RBFS it prints f_limit, best, alternative, current-city and next-city for each node visited.


