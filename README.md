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

---

## Kruskal
Kruskal's algorithm is a greedy algorithm used to find the Minimum Spanning Tree (MST) of a connected, undirected, weighted graph. It operates by sorting all graph edges in non-decreasing order of their weights and iteratively adding the lightest edge to the MST, provided it does not form a cycle.To efficiently detect and prevent cycles, the algorithm utilizes a Disjoint Set Union (DSU) / Union-Find data structure optimized with path compression and union by rank.
If a node or edge fails (becomes un-traversable), the algorithm filters out the missing components prior to sorting and running DSU. If a failure splits the graph into disconnected subgraphs, the algorithm gracefully adapts by returning a Minimum Spanning Forest (MSF). Here are the results from the graph in the assignment
---
### Initial State
The graph consists of 7 vertices initialized as isolated sets: {A}, {B}, {C}, {D}, {E}, {F}, {G}. All 12 edges are sorted by weight, and the algorithm targets selecting 7 - 1 = 6 edges.
---
### Iteration 1: Edge (A, G), Weight 5
The algorithm evaluates the lightest edge (A, G). Since A and G are in separate sets, adding this edge creates no cycle. The DSU performs a union, merging them into component {A, G}.
---
### Iteration 2: Edge (B, C), Weight 5
The algorithm checks (B, C). Vertices B and C belong to disjoint sets, so the edge is accepted. The DSU merges them into component {B, C}.
---
### Iteration 3: Edge (D, E), Weight 5
The algorithm checks (D, E). Nodes D and E are currently in separate components, so the edge is added. The DSU merges them into component {D, E}.
---
### Iteration 4: Edge (E, F), Weight 5
The algorithm evaluates (E, F). Vertex E is in component {D, E} while F is isolated. Since their roots differ, the edge is accepted, expanding the component to {D, E, F}.
---
### Iteration 5: Edge (A, C), Weight 6
The algorithm considers (A, C). Vertex A belongs to {A, G} and C belongs to {B, C}. Because these are two distinct components, the edge is accepted, merging them into {A, B, C, G}.
---
### Iteration 6: Edge (F, G), Weight 6
The algorithm evaluates (F, G). Vertex F belongs to {D, E, F} and G belongs to {A, B, C, G}. Since they are in separate components, the edge is added, connecting all vertices into a single component {A, B, C, D, E, F, G}.
---
### Iteration 7: Remaining Edges & Termination
With 6 edges selected, the MST is complete. Any further evaluation of the remaining edges (A, B), (B, D), (C, E), (B, E), (C, F), (A, F), reveals that both endpoints already share the same root, so they are rejected to prevent cycles. The process terminates with a total weight of 32.

---

## Prim








AI tools usage disclosure:

https://claude.ai/share/bc5bca97-f9e8-4683-a52f-9ef00529fdfe

https://claude.ai/share/d46f5fb3-1aa6-4a6f-b784-8654c2a9e618
