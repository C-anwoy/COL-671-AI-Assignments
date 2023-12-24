# Game Playing AI Agent for Connect4 Game

The objective is to implement an AI agent for playing a two-player game, and the challenge is to plan in the presence of an adversary with a budget on the computation allowed before performing a decision/move.

## Problem Analysis:


Consider a  (m x n) board, and assume that each player has ‘p’ pop-out moves initially. 
Then, the maximum depth of the game tree (D) = Total number of moves required by both players so that no valid move is remaining for each player

Therefore, D = mn + 4p

And, the branching factor of the game tree (b) = number of valid moves available
Now, the number of valid moves available = [(number of columns with at least one empty cell) + (number of pop-out moves available for the player)]
Hence, maximum number of valid moves available at any node = (n + p)

Therefore, b = n+p

As we are given a time-out for each move, clearly we cannot expand the entire tree for larger board sizes. If the time-out given be ‘t’ seconds, and in this time we can expand up to  depth ‘d’, then we observe that d is actually a function of the total number of valid moves available at maximum for a node (V) and the time-out given (t), i.e., d = f(V, t).

Further, we observe, V = n+p . 

So, it can be concluded that d = g(n, p, t), i.e. the depth upto which we can expand the game tree in the given threshold time depends on the number of columns in the board, 
number of pop-out moves available at the start, and the time-out given.

Hence, the number of nodes expanded by our algorithm will be = N = O((n+p)^d)

## PART-A: Expectimax Agent

As we know, in the standard Expectimax Algorithm, the MAX nodes (nodes corresponding to moves by our agent) remain as it was in the Minimax algorithm, and the MIN nodes 
(nodes corresponding to moves by the opponent) are replaced by CHANCE nodes, which take value equal to the average of the possible scores of its children, and all moves are considered 
equally probable at the CHANCE nodes, hence any one move is selected at random considering an underlying uniform probability distribution for the available valid movie.

For the expectimax agent, we have implemented an “Iterative Deepening Expectimax Algorithm”. During every iteration of the algorithm, we are keeping track of the time left; and if during 
an iteration time-out occurs, then we return the best move obtained in the previous iteration which was completed.

Now, in the d-th iteration of the algorithm, the cut-off depth is d, i.e. the nodes at depth are considered as leaf nodes and the tree is not expanded further. So, to estimate, or, 
approximate a score for nodes at depth d we use a Heuristic (also called ‘Evaluation function’).


### Heuristic/Evaluation function: 

The Evaluation function we have formulated is:

EVAL(s) = 20*(n4,1(s) - n4,2(s)) + 5*(n3,1(s) - n3,2(s)) + 2*(n2,1(s) - n2,2(s))

[Note that the evaluation function is EVAL(s) when our agent is player 1, and -EVAL(s) when our agent is player 2]

where, ni,j(s) = total number of i consecutive tokens (vertically, horizontally and diagonally) of player j in a board configuration obtained by filling all the empty cells in the board 
corresponding to state s with the token of player j.

Clearly, the evaluation function used [i.e., EVAL(s)] is an optimistic estimate of the score of the states corresponding to the nodes at the cut-off depth. 

## PART-B: Adversarial Agent

For the adversarial agent, we have implemented an “Iterative Deepening Minimax Algorithm with Alpha-Beta Pruning”. 

During every iteration of the algorithm, we are keeping track of the time left; and if during an iteration time-out occurs, then we return the best move obtained in the previous 
iteration which was completed. Also, we are using the information gained during an iteration of the algorithm to expand the tree more efficiently (i.e., we use the information from the previous iteration to get a more tight upper bound on the score at each node, and so alpha-beta pruning works better) during the next iteration. 

While testing our algorithm, we found it to be consistently winning against the standard minimax algorithm with alpha-beta pruning.


- 	As we know, when we use alpha-beta pruning in the standard minimax algorithm, alpha gives the lower bound that the maximizer currently can guarantee at that level or above, 
	and beta is the best value that the minimizer currently can guarantee at that level or above. 

### Idea used in our algorithm : 

-	Now, in our algorithm, as we do iterative deepening, we get some values for alpha and beta at every state (or, node) for an iteration. 
-	We store this value [alpha for the max nodes and beta for the min nodes] in a dictionary with the unique state representation as the key. 
-	Now in the next iteration of the algorithm, the upper bound ‘beta’ we start with at each node is the minimum among the current beta and the value stored in the dictionary from 
	the previous iteration. 

In this way, the dictionary is updated in each iteration and we use the information gathered in previous iterations to get a tighter upper bound which results in more efficient 
pruning as alpha-beta pruning technique is used - this helps us to expand to more depth compared to using standard alpha-beta pruning which starts with no information about the nodes 
in the game tree.

Now, in the d-th iteration of the algorithm, the cut-off depth is d, i.e. the nodes at depth are considered as leaf nodes and the tree is not expanded further. 
So, to estimate, or, approximate a score for nodes at depth d we use a Heuristic (also called ‘Evaluation function’).


### Heuristic/Evaluation function: 

 The Evaluation function used in this case is the same as the one discussed above in the case of Expectimax agent.

