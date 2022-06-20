# uninformed-search-algorithms
Comparison of Breadth First Search, Depth First Search, Depth Limited and Iterative Depth Limited algorithms according to their expanded node counts and max fringe sizes while they solve 8 puzzle game.

## Usage
Enter start state to start_state variable in Agent.py at line 270 as 2d list. Code will print all outputs.

Coded in python 3

### Example Output
```
Start State:
[4,2,0,]
[1,3,8,]
[6,5,7,]

Breadth First
Count of expanded nodes: 4387
Max fringe size: 5023
[0,1,2,]
[3,4,5,]
[6,7,8,]

Depth Limited
Count of expanded nodes: 743
Max fringe size: 17
[0,1,2,]
[3,4,5,]
[6,7,8,]

Iterative Depth Limit
Count of expanded nodes: 3694
Max fringe size: 17
[0,1,2,]
[3,4,5,]
[6,7,8,]

Depth first cant solve it
```
