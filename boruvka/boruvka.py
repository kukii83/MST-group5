from collections import defaultdict

# 1. Graph definition (from the given assignment)

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

# 2. Union-Find (Disjoint Set Union) helper

class DSU:
    """Union-Find with path compression + union by rank."""

    def __init__(self, nodes):
        self.parent = {n: n for n in nodes}
        self.rank = {n: 0 for n in nodes}

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # path compression
            x = self.parent[x]
        return x

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True


# 3. Boruvka's Algorithm

def boruvka_mst(nodes, edges, verbose=True):
    """
    Runs Boruvka's algorithm.

    Returns:
        mst_edges: list of (u, v, w) chosen for the MST/MSF
        total_weight: sum of weights
        trace: list of dict, one per round, describing what happened
               (used to build the report table)
    """
    dsu = DSU(nodes)
    mst_edges = []
    trace = []
    num_components = len(nodes)
    round_no = 0

    if verbose:
        print(f"Boruvka's Algorithm on {len(nodes)} nodes, {len(edges)} edges")
        print("=" * 70)

    while num_components > 1:
        round_no += 1
        # cheapest[component_root] = (weight, u, v)
        cheapest = {}

        for (u, v, w) in edges:
            ru, rv = dsu.find(u), dsu.find(v)
            if ru == rv:
                continue  # already same component, would form a cycle
            if ru not in cheapest or w < cheapest[ru][0]:
                cheapest[ru] = (w, u, v)
            if rv not in cheapest or w < cheapest[rv][0]:
                cheapest[rv] = (w, u, v)

        if not cheapest:
            # No edge connects the remaining components then graph is
            # disconnected. Stop here, result is a minimum spanning forest.
            if verbose:
                print(f"Round {round_no}: no connecting edge found for some "
                      f"component(s) -> graph is disconnected. Stopping.")
            trace.append({
                "round": round_no,
                "components_before": components_snapshot(dsu, nodes),
                "chosen_edges": [],
                "note": "disconnected - no further merge possible",
                "components_after": components_snapshot(dsu, nodes),
            })
            break

        components_before = components_snapshot(dsu, nodes)
        chosen_this_round = []

        # Add each cheapest edge once (guard against adding the same edge
        # twice when it is cheapest for both of its endpoints' components)
        added_pairs = set()
        for root, (w, u, v) in cheapest.items():
            key = tuple(sorted((u, v))) + (w,)
            if key in added_pairs:
                continue
            if dsu.find(u) != dsu.find(v):
                dsu.union(u, v)
                mst_edges.append((u, v, w))
                chosen_this_round.append((u, v, w))
                added_pairs.add(key)

        num_components = len({dsu.find(n) for n in nodes})
        components_after = components_snapshot(dsu, nodes)

        if verbose:
            print(f"Round {round_no}:")
            print(f"  Components before : {components_before}")
            print(f"  Cheapest edges chosen : {chosen_this_round}")
            print(f"  Components after  : {components_after}")
            print("-" * 70)

        trace.append({
            "round": round_no,
            "components_before": components_before,
            "chosen_edges": chosen_this_round,
            "note": "",
            "components_after": components_after,
        })

    total_weight = sum(w for _, _, w in mst_edges)
    return mst_edges, total_weight, trace


def components_snapshot(dsu, nodes):
    """Return components as a sorted list of sorted-tuples"""
    groups = defaultdict(list)
    for n in nodes:
        groups[dsu.find(n)].append(n)
    return sorted([tuple(sorted(g)) for g in groups.values()])


def run_scenario(name, nodes, edges, verbose=False):
    print(f"Nodes ({len(nodes)}): {nodes}")
    print(f"Edges ({len(edges)}): {edges}")
    mst_edges, total, trace = boruvka_mst(nodes, edges, verbose=verbose)
    connected = (len(mst_edges) == len(nodes) - 1)
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



# 4. Manual / interactive graph input

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

        # Accept commas, spaces, or both as separators.
        tokens = [t.strip() for t in raw.replace(",", " ").split()]
        tokens = [t for t in tokens if t]  # drop empties

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
    print("Format: <node1> <node2> <weight>   e.g.  A B 7")
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
            # Store as int if it's a whole number, for cleaner display.
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
            "Enter 1 or 2: "
        ).strip()

        if choice == "1":
            return build_graph_from_user()
        elif choice == "2":
            return ALL_NODES, ORIGINAL_EDGES
        else:
            print("  -> Please type 1 or 2.")


if __name__ == "__main__":
    nodes, edges = choose_graph_source()

    print()
    result = run_scenario("User-provided graph", nodes, edges, verbose=True)

    if not result["fully_connected"]:
        print(
            "\nNote: the graph you entered is disconnected, so the result "
            "above is a Minimum Spanning FOREST (not a single spanning tree)."
        )
