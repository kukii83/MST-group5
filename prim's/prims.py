from collections import defaultdict
import heapq

# ---------------------------------------------------------------------------
# 1. Graph definition (from the given assignment)
# ---------------------------------------------------------------------------

ORIGINAL_EDGES = [
    ("A", "B", 7),
    ("A", "C", 6),
    ("A", "F", 10),
    ("A", "G", 5),
    ("B", "C", 5),
    ("B", "D", 7),
    ("B", "E", 9),
    ("C", "E", 7),
    ("C", "F", 9),
    ("D", "E", 5),
    ("E", "F", 5),
    ("F", "G", 6),
]

ALL_NODES = ["A", "B", "C", "D", "E", "F", "G"]


# ---------------------------------------------------------------------------
# 2. Prim's Algorithm
# ---------------------------------------------------------------------------

def build_adjacency_list(nodes, edges):
    """Converts an edge list into an adjacency list representation."""
    adj = {n: {} for n in nodes}
    for u, v, w in edges:
        if u in adj and v in adj:
            adj[u][v] = w
            adj[v][u] = w
    return adj


def get_current_components(visited, nodes, adj):
    """Finds connected components for reporting (handles MSF if graph is disconnected)."""
    # For Prim, we can do a quick connected-components scan using BFS/DFS on unvisited/visited partitions
    visited_set = set(visited)
    all_nodes_set = set(nodes)
    
    # Let's find connected components of the overall graph or just the visited subgraph
    # To keep it consistent with the snapshot view:
    parent = {n: n for n in nodes}
    def find(i):
        if parent[i] == i:
            return i
        parent[i] = find(parent[i])
        return parent[i]
    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            parent[root_i] = root_j

    # Union based on valid edges in the graph or built MST edges
    groups = defaultdict(list)
    for n in nodes:
        groups[find(n)].append(n)
    return sorted([tuple(sorted(g)) for g in groups.values()])


def prim_mst(nodes, edges, start_node=None, verbose=True):
    """
    Runs Prim's algorithm using a min-heap.

    Returns:
        mst_edges: list of (u, v, w) chosen for the MST/MSF
        total_weight: sum of weights
        trace: list of dict, one per step evaluated
    """
    adj = build_adjacency_list(nodes, edges)
    
    if not nodes:
        return [], 0, []

    if start_node is None or start_node not in nodes:
        start_node = nodes[0]

    visited = set()
    mst_edges = []
    trace = []
    step_no = 0

    if verbose:
        print(f"Prim's Algorithm on {len(nodes)} nodes, {len(edges)} edges (Start node: {start_node})")
        print("=" * 70)

    # To handle potential disconnected graphs (MSF), we loop over all nodes
    unvisited_nodes = set(nodes)

    while unvisited_nodes:
        # If the current component is exhausted but nodes remain, pick a new start node
        if not visited:
            current_start = unvisited_nodes.pop()
            visited.add(current_start)
            if verbose:
                print(f"Starting new component at node: {current_start}")
            
            # Priority queue stores tuples of: (weight, u, v)
            pq = []
            for neighbor, weight in adj[current_start].items():
                if neighbor in unvisited_nodes:
                    heapq.heappush(pq, (weight, current_start, neighbor))
            continue

        if not pq:
            # If priority queue is empty and there are still unvisited nodes, graph is disconnected
            if unvisited_nodes:
                current_start = unvisited_nodes.pop()
                visited.add(current_start)
                if verbose:
                    print(f"Graph disconnected. Starting new component at node: {current_start}")
                for neighbor, weight in adj[current_start].items():
                    if neighbor in unvisited_nodes:
                        heapq.heappush(pq, (weight, current_start, neighbor))
                continue
            else:
                break

        step_no += 1
        weight, u, v = heapq.heappop(pq)

        # If v is already visited, this edge would form a cycle
        if v in visited:
            status = f"REJECTED (Node {v} already visited - forms cycle)"
            if verbose:
                print(f"Step {step_no}: Edge evaluated ({u}, {v}) weight {weight}")
                print(f"  Status             : {status}")
                print("-" * 70)
            trace.append({
                "step": step_no,
                "edge": (u, v, weight),
                "status": status,
            })
            continue

        # Otherwise, add v to visited and include edge in MST
        visited.add(v)
        unvisited_nodes.discard(v)
        mst_edges.append((u, v, weight))
        status = "ADDED (Safe edge)"

        if verbose:
            print(f"Step {step_no}: Edge evaluated ({u}, {v}) weight {weight}")
            print(f"  Status             : {status}")
            print(f"  Visited nodes      : {sorted(list(visited))}")
            print("-" * 70)

        trace.append({
            "step": step_no,
            "edge": (u, v, weight),
            "status": status,
            "visited_so_far": sorted(list(visited))
        })

        # Push all edges from the newly added vertex v to unvisited neighbors
        for neighbor, w in adj[v].items():
            if neighbor not in visited:
                heapq.heappush(pq, (w, v, neighbor))

    total_weight = sum(w for _, _, w in mst_edges)
    return mst_edges, total_weight, trace


def run_scenario(name, nodes, edges, start_node=None, verbose=False):
    print(f"Nodes ({len(nodes)}): {nodes}")
    print(f"Edges ({len(edges)}): {edges}")
    mst_edges, total, trace = prim_mst(nodes, edges, start_node=start_node, verbose=verbose)
    connected = (len(mst_edges) == len(nodes) - 1) if nodes else True
    print(f"Resulting MST/MSF edges: {mst_edges}")
    print(f"Total weight: {total}")
    print(f"Graph fully connected by result: {connected}")
    return {
        "name": name,
        "nodes": nodes,
        "edges": edges,
        "mst_edges": mst_edges,
        "total_weight": total,
        "trace": trace,
        "fully_connected": connected,
    }


# ---------------------------------------------------------------------------
# 3. Manual / interactive graph input (Same format as friend's script)
# ---------------------------------------------------------------------------

def get_nodes_from_user():
    """Prompt the user for a list of node names (comma or space separated)."""
    while True:
        raw = input(
            "Enter node names separated by commas or spaces "
            "(e.g. A,B,C,D): "
        ).strip()
        if not raw:
            print("  -> You must enter at least one node. Try again.")
            continue

        tokens = [t.strip() for t in raw.replace(",", " ").split()]
        tokens = [t for t in tokens if t]

        if not tokens:
            print("  -> No valid node names found. Try again.")
            continue

        if len(set(tokens)) != len(tokens):
            print("  -> Duplicate node names detected. Please use unique names.")
            continue

        return tokens


def get_edges_from_user(nodes):
    """
    Prompt the user for edges one at a time, in the form:
        u v w
    e.g.  A B 7
    Type 'done' (or leave blank) when finished.
    """
    node_set = set(nodes)
    edges = []

    print("\nNow enter the edges of the graph.")
    print("Format: <node1> <node2> <weight>    e.g.  A B 7")
    print("Type 'done' (or press Enter on an empty line) when you're finished.\n")

    while True:
        raw = input(f"Edge #{len(edges) + 1} (or 'done'): ").strip()

        if raw == "" or raw.lower() == "done":
            if len(edges) == 0:
                print("  -> You need at least one edge before finishing.")
                continue
            break

        parts = raw.replace(",", " ").split()
        if len(parts) != 3:
            print("  -> Please enter exactly: node1 node2 weight (e.g. A B 7)")
            continue

        u, v, w_raw = parts

        if u not in node_set or v not in node_set:
            print(f"  -> '{u}' or '{v}' is not one of your declared nodes: "
                  f"{sorted(node_set)}. Try again.")
            continue

        if u == v:
            print("  -> Self-loops (u == v) aren't allowed for MST. Try again.")
            continue

        try:
            w = float(w_raw)
            if w.is_integer():
                w = int(w)
        except ValueError:
            print(f"  -> '{w_raw}' is not a valid number for the weight. Try again.")
            continue

        edges.append((u, v, w))
        print(f"  -> Added edge: {u} -- {v}  (weight {w})")

    return edges


def build_graph_from_user():
    """Runs the full interactive prompt sequence and returns (nodes, edges)."""
    print("=" * 70)
    print("MANUAL GRAPH INPUT")
    print("=" * 70)
    nodes = get_nodes_from_user()
    edges = get_edges_from_user(nodes)
    return nodes, edges


def choose_graph_source():
    """
    Lets the user pick between typing in their own graph or using the
    graph from the assignment.
    """
    while True:
        choice = input(
            "\nChoose graph source:\n"
            "  [1] Enter my own graph manually\n"
            "  [2] Use the built-in example graph\n"
        ).strip()

        if choice == "1":
            return build_graph_from_user()
        elif choice == "2":
            return ALL_NODES, ORIGINAL_EDGES
        else:
            print("  -> Please type 1 or 2.")


if __name__ == "__main__":
    nodes, edges = choose_graph_source()

    start_node = input(f"Enter starting node for Prim's (default '{nodes[0]}'): ").strip()
    if not start_node or start_node not in nodes:
        start_node = nodes[0]

    print()
    result = run_scenario("User-provided graph", nodes, edges, start_node=start_node, verbose=True)

    if not result["fully_connected"]:
        print(
            "\nNote: the graph you entered is disconnected, so the result "
            "above is a Minimum Spanning FOREST (not a single spanning tree)."
        )
