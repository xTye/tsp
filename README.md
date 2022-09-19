# Traveling Salesman Problem
##### Spreading wealth using the worst case solution.

## Introduction
Hello, this is an attempt to solve the Traveling Salesman Problem with a polynomial time solution. The idea for this solution struck during my COP 4210 - Discrete Structures II class at the University of Central Florida taught by Professor Matthew Gerber.

**Side bar**

I often struggle with the idea of learning things. I've noticed it takes me about 3 or 4 times of repitition before completely understandig things. However, over the years of my college experience, I've taken note that I learn better by not learning what is, but learning what isn't. Everytime I struggle with math, it's usually because teachers either don't explain the conceptual topics of *why* the math is the way it is or don't explicity point out the difference between current and new knowledge. For example, it would be nice to iteratively repeat the importance of complex numbers and their significance in contructing wave functions and *why* we use trigonometry to understand and describe the fundamental nature of waves in different coordinate systems. From my experience, not enough teachers do this, which is why I spend my own free time finding these connections and answers to my own questions, where teachers can't do themself.

During the Discrete course I was experiencing this feeling again, and found myself stuck on understanding complexity classes. It bothers me that there is no definate proof to the `P=NP` complexity problems. I thought that reading my textbook might give me more insight, but after the tenth reread on the significance of different problem sets, I realized the sheer uncertainty that mathematicians have to understand systems. Personally, I never though that proof by reduction was a strong argument, and boiling down many problem sets to NP-Complete is dangerous, becasue of its lack of proof in relation to solving things in polynomial time. After all, there are different ways to solve the same problem.

## The Solution - Sometimes

The inspiraiton behind this solution is very simple. Consider the worst case, pick the best solution.

**Given**
> The graph is complete
> 
> There is one hamiltonian cycle

Because the graph is complete, there must be a hamiltonian cycle. This being said, we don't have to worry about traversing the path to find a hamiltonian cycle to consider if there is a path, we can treat the nodes seperately, picking its entry and output points respectfully, and widdling down the edge selections, until there aren't anymore to choose from.

**Sum the nodes**

Take your graph, a *NxN* matrix, where the intersection between two outer nodes have an edge. Nodes cannot have an edge between themselves, so we can mark there edge weight as zero.

    A 0 6725 5474 3237 5566 7594 6510 3221 9257 6624 4132
    B 6725 0 2372 2209 8280 1657 3674 5360 9487 6959 186
    C 5474 2372 0 9985 5987 3691 9523 2184 891 1488 2113
    D 3237 2209 9985 0 3587 3906 2694 3360 8328 3074 6402
    E 5566 8280 5987 3587 0 2662 985 3740 7800 6208 3103
    F 7594 1657 3691 3906 2662 0 2010 654 2638 5658 3515
    G 6510 3674 9523 2694 985 2010 0 9095 3702 4145 9118
    H 3221 5360 2184 3360 3740 654 9095 0 4628 6166 2901
    I 9257 9487 891 8328 7800 2638 3702 4628 0 2228 7582
    J 6624 6959 1488 3074 6208 5658 4145 6166 2228 0 5239
    K 4132 186 2113 6402 3103 3515 9118 2901 7582 5239 0

> NOTE
> 
> The top and bottom half of these graph forms two equal triangles where every node has an edge weight with every other node.

To get the sum, add up the columns or the rows, the result should be the same for both.

    A 0 6725 5474 3237 5566 7594 6510 3221 9257 6624 4132 = 58340
    B 6725 0 2372 2209 8280 1657 3674 5360 9487 6959 186  = 46909
    C 5474 2372 0 9985 5987 3691 9523 2184 891 1488 2113  = 43708
    D 3237 2209 9985 0 3587 3906 2694 3360 8328 3074 6402 = 46782
    E 5566 8280 5987 3587 0 2662 985 3740 7800 6208 3103  = 47918
    F 7594 1657 3691 3906 2662 0 2010 654 2638 5658 3515  = 33985
    G 6510 3674 9523 2694 985 2010 0 9095 3702 4145 9118  = 51456
    H 3221 5360 2184 3360 3740 654 9095 0 4628 6166 2901  = 41309
    I 9257 9487 891 8328 7800 2638 3702 4628 0 2228 7582  = 56541
    J 6624 6959 1488 3074 6208 5658 4145 6166 2228 0 5239 = 47789
    K 4132 186 2113 6402 3103 3515 9118 2901 7582 5239 0  = 44291

**Sort the nodes**

Sort the nodes in worst case to best case scenario. The result is going to contribute to how the nodes are selected in the algorithm, where we should be picking the worst node first.

    A 0 6725 5474 3237 5566 7594 6510 3221 9257 6624 4132 = 58340
    I 9257 9487 891 8328 7800 2638 3702 4628 0 2228 7582  = 56541
    G 6510 3674 9523 2694 985 2010 0 9095 3702 4145 9118  = 51456
    E 5566 8280 5987 3587 0 2662 985 3740 7800 6208 3103  = 47918
    J 6624 6959 1488 3074 6208 5658 4145 6166 2228 0 5239 = 47789
    B 6725 0 2372 2209 8280 1657 3674 5360 9487 6959 186  = 46909
    D 3237 2209 9985 0 3587 3906 2694 3360 8328 3074 6402 = 46782
    K 4132 186 2113 6402 3103 3515 9118 2901 7582 5239 0  = 44291
    C 5474 2372 0 9985 5987 3691 9523 2184 891 1488 2113  = 43708
    H 3221 5360 2184 3360 3740 654 9095 0 4628 6166 2901  = 41309
    F 7594 1657 3691 3906 2662 0 2010 654 2638 5658 3515  = 33985
    
**Groups / Linked Lists**

To pick the best options from the worst node, we need some sort of system to handle the grouping mechanisms for situations where A already has an input and output. So, I created a system with groups, that act as a Linked List, to ensure the nodes that aren't a start or end are rejected from the selection pool. There can relistically be less than twice the groups as there are nodes, because every group has to have at least 3 nodes, meaning there can at most be N/3 groups, but it rarely happens that there are this many groups. Notably, we must combine two groups that have the same edge node. As a result, we avoid potential edge nodes from being on an edge on one group and in the middle of another group. Therefore, we *must* connect the two groups if we can.

The most basic group looks like this: `A-B-C` where A and C are the outer nodes in group. B has both input and output edges, and cannot have anymore edges.
> Note
>
> A and C need an input and output edge respectively, to complete the hamiltonian cycle.

**Iterations**

Psuedocode:
    Check if biggest group size has N nodes
      break
    Pick the next worst node
    Check if it is in the middle of a group
      next node
    Check if its on an edge
      find the other input / output edge - that is not going to close off current group size has N nodes
      check if other input / output edge can connect to another group
        merge groups
    Otherwise, create a new group
      find input edge
      check if input edge exists on another group
        merge groups
      find output edge - that is not going to close off current group unless group size has N nodes
      check if output edge can connect to another group
        merge groups

> NOTE
>
> The order in the groups doesn't matter since the graph is bidirectional.

### 1: Choose A
Create new group

-A-

-A-H

D-A-H


**Current Groups:**

D-A-H

### 2: Choose I
Create new group

-I-

C-I-

C-I-J


**Current Groups:**

D-A-H

C-I-J

### 3: Choose G
Create new group

-G-

-G-D


Merge groups

-G-D and D-A-H

-G-D-A-H

Find input node

E-G-D-A-H


**Current Groups:**

E-G-D-A-H

C-I-J

### 4: Choose E
Find input edge

-E-G-D-A-H

K-E-G-D-A-H

> NOTE
>
> Node D was skipped because it already has input and output edges.


**Current Groups:**

K-E-G-D-A-H

C-I-J

### 5: Choose J
Find output edge

C-I-J-

C-I-J-K

> NOTE
>
> Node C was skipped because it would close of the group, meaning that group wouldn't be able to merge with other groups later on.
>
> Node D was skipped because it already has input and output edges.
>
> Node G was skipped because it already has input and output edges.

Merge groups

C-I-J-K and K-E-G-D-A-H

C-I-J-K-E-G-D-A-H


**Current Groups:**

C-I-J-K-E-G-D-A-H

### 6: Choose B
Create new group

-B-

-B-F

> NOTE
>
> Node K was skipped because it already has input and output edges.

C-B-F

> NOTE
>
> Node D was skipped because it already has input and output edges.

Merge groups

C-B-F and C-I-J-K-E-G-D-A-H

F-B-C-I-J-K-E-G-D-A-H


**Current Groups:**

F-B-C-I-J-K-E-G-D-A-H

### Finished
F-B-C-I-J-K-E-G-D-A-H

End node next is start node

F-B-C-I-J-K-E-G-D-A-H-F

This yields (with around 15% accuracy) the shortest path. To get the total sum of this path, traverse through the linked list and add the edge weights.

## Conclusion
After running the `combined.py` script that takes the non-polynomial time solution and my solution and compares the result sum to each other. The results show about 15% accuracy when using both integers and decimal solutions as a sample pool of 11 nodes. The non-polynomial time solution can only calculate 11 nodes within a reasonable time. Anymore nodes than that, and the runtime has a noticable realtime affect on calculation times. Notably, this solution does become more accurate with the lower amounts of nodes, but nonetheless has shown more solidarity in the takeaways more than anything else.

### Takeaways
This was a fun experiment. While I did learn what its like to have a taste of existential humility, I didn't give up hope to find a polynomial solution. After all, it is correct... sometimes. I think this algorithm can be built on, maybe to not provide a solution with *100%* accuracy, but with *99.999%* accuracy. This includes things like taking multiple polynomial time solutions and merging them together. As well as researching other solutions, learning from their algorithms and modifying them.

Additionally, its important to note that tradeoffs happen when picking an edge, perhaps if I were to weigh the value in tradeoffs of each time an edge weight is picked, then we can influence the overall sum of the path.

#### Thoughful Questions
> How could we design an elo system to rate the value of the edges?

> How much stake will we risk when picking an edge N from another edge M, that may have a diminishing return on a potential path that M had, that is otherwise lost?

>In the case of merging multiple polynomial time solutions, will this create a runtime that is thereotically the limit of a non-polynomial time solution?

>How will this relate the accuracy of the algorithm?
