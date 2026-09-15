# ITS Graph Theory class Group 5

Group 5 Members:

-Maulana Anugra Putra/5025251159 (kukii83)

-I Gusti Agung Candra Nugraha/5025251169 (candranugraha576)

-Hussein Mohammad Mahsun/5025251170 (TheDelightOFice)



In this task, we are using three algorithms to use three algorithms, that is:
- Boruvka
- Kruskal
- Prim

---

## Boruvka
Boruvka's Algorithm is a well-known greedy approach for finding the Minimum Spanning Tree or Minimum Spanning Forest in a weighted, undirected graph.

How It Works:

1. Begin with each vertex in its own separate component.
   
2. In each round, look at all the connected groups and find the lightest edge that connects each group to another group outside of it.
   
3. Combine all selected edges at once into the minimum spanning tree and use a Disjoint Set Union (DSU / Union-Find) structure to join the components together.
   
4. Keep repeating the process until all the vertices are joined into one connected group (1 MST) or there are no more edges left to connect them (MSF). The time complexity is O(E log V), where E represents the total number of edges and V represents the total number of vertices.
   
A key feature is that it can be easily done in parallel because each round can choose edges for different parts at the same time without needing to wait for others.

### Prerequisites
-Python 3.x +

-No external third-party dependencies required

### Instructions
1. Clone or download this repository containing boruvka.py.

2.Open your terminal or command prompt in the project directory.

3.Execute the script: 

```
python boruvka.py
```

4. Choose the input mode when prompted; Enter 1 to manually input custom nodes and weighted edges.  Enter 2 to run the algorithm using the built-in default graph.  

### Results

<img width="2028" height="588" alt="image" src="https://github.com/user-attachments/assets/92912af4-242d-47c8-babc-7c0094e0487e" />

Vizualised it would look like this:

<img width="367" height="313" alt="image" src="https://github.com/user-attachments/assets/1ff910de-35bb-4cb5-872a-dbde5c205d7a" />


**Final MST edges**: (A-G)=5, (B-C)=5, (E-F)=5, (D-E)=5, (A-C)=6, (F-G)=6

**Total MST weight**: 32

---

## Kruskal
Kruskal's algorithm is a greedy algorithm used to find the Minimum Spanning Tree (MST) of a connected, undirected, weighted graph. It operates by sorting all graph edges in non-decreasing order of their weights and iteratively adding the lightest edge to the MST, provided it does not form a cycle.To efficiently detect and prevent cycles, the algorithm utilizes a Disjoint Set Union (DSU) / Union-Find data structure optimized with path compression and union by rank.
If a node or edge fails (becomes un-traversable), the algorithm filters out the missing components prior to sorting and running DSU. If a failure splits the graph into disconnected subgraphs, the algorithm gracefully adapts by returning a Minimum Spanning Forest (MSF). 

### Prerequisites
- Python 3.x interpreter installed
- Standard Python built-in libraries

### Instructions
- Copy the code
- Open your compiler(make sure it's not DevC++ or anything since this is a Phyton code)
- Paste the code
- Run the code
- Pick option 2 for the graph in the assignment

### Results
Here are the results from the graph in the assignment:

- **Initial State** |
The graph consists of 7 vertices initialized as isolated sets: {A}, {B}, {C}, {D}, {E}, {F}, {G}. All 12 edges are sorted by weight, and the algorithm targets selecting 7 - 1 = 6 edges.

- **Iteration 1: Edge (A, G), Weight 5** |
The algorithm evaluates the lightest edge (A, G). Since A and G are in separate sets, adding this edge creates no cycle. The DSU performs a union, merging them into component {A, G}.

- **Iteration 2: Edge (B, C), Weight 5** |
The algorithm checks (B, C). Vertices B and C belong to disjoint sets, so the edge is accepted. The DSU merges them into component {B, C}.

- **Iteration 3: Edge (D, E), Weight 5** |
The algorithm checks (D, E). Nodes D and E are currently in separate components, so the edge is added. The DSU merges them into component {D, E}.

- **Iteration 4: Edge (E, F), Weight 5** |
The algorithm evaluates (E, F). Vertex E is in component {D, E} while F is isolated. Since their roots differ, the edge is accepted, expanding the component to {D, E, F}.

- **Iteration 5: Edge (A, C), Weight 6** |
The algorithm considers (A, C). Vertex A belongs to {A, G} and C belongs to {B, C}. Because these are two distinct components, the edge is accepted, merging them into {A, B, C, G}.

- **Iteration 6: Edge (F, G), Weight 6** |
The algorithm evaluates (F, G). Vertex F belongs to {D, E, F} and G belongs to {A, B, C, G}. Since they are in separate components, the edge is added, connecting all vertices into a single component {A, B, C, D, E, F, G}.

- **Iteration 7: Complete** |
With 6 edges selected, the MST is complete. Any further evaluation of the remaining edges (A, B), (B, D), (C, E), (B, E), (C, F), (A, F), reveals that both endpoints already share the same root, so they are rejected to prevent cycles. The process terminates with a total weight of 32.


---

## Prim
Prim’s Algorithm is a greedy algorithm used to find a Minimum Spanning Tree (MST) for a weighted, undirected graph.
Unlike Kruskal's algorithm (which sorts all edges globally), Prim's grows a single tree outward step-by-step from a starting Node, always picking the lowest weight edge that connects a visited Node to an unvisited one until all nodes are connected.

### How it works:
 - **Start:** Choose any node as your starting point and mark it as visited.
 - **Look around:** Check all the edges connected to your visited nodes that lead to unvisited nodes.
 - **Pick the smallest:** Choose the edge with the lowest weight.
 - **Repeat:** Add that new node to your visited group, include the edge in your tree, and repeat steps 2–3 until every node has been visited.

### Prerequisites
-Python 3.x +

-No external third-party dependencies required

### Instructions
1. Clone or download this repository containing prims.py.
   
2. Open your terminal or command prompt in the project directory.

3. Execute the script: 

```
python prims.py
```

4. Choose the input mode when prompted; Enter 1 to manually input custom nodes and weighted edges.  Enter 2 to run the algorithm using the built-in default graph.  

### Results
<img width="1537" height="861" alt="image" src="https://github.com/user-attachments/assets/16496cd5-f187-498e-8eba-b37f11d829f0" />

Vizualised it would look like this:

<img width="724" height="589" alt="image" src="https://github.com/user-attachments/assets/302ebf3e-4d27-40a7-9e69-23ffd2de44bf" />

**Final MST edges**: (A-G)=5, (A-C)=6, (C-B)=5, (G-F)=6, (F-E)=5, (E-D)=5

**Total MST weight**: 32

---

AI tools usage disclosure:

https://claude.ai/share/bc5bca97-f9e8-4683-a52f-9ef00529fdfe

https://claude.ai/share/d46f5fb3-1aa6-4a6f-b784-8654c2a9e618

https://share.gemini.google/LZn3BaogJ0mE
