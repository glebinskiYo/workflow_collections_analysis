import networkx as nx
from pathlib import Path
from collections import deque

ROOT = Path(__file__).resolve().parent.parent

print("Loading DAG...")

dot_graph = nx.drawing.nx_pydot.read_dot(
    ROOT / "data" / "ampliseq.dot"
)

processes = {}

for node, attrs in dot_graph.nodes(data=True):

    label = attrs.get(
        "label",
        ""
    ).strip('"')

    if (
        "NFCORE_AMPLISEQ:AMPLISEQ:"
        not in label
    ):
        continue

    processes[node] = (
        label.split(":")[-1]
        .lower()
    )

dependencies = set()

for source_node, source_process in processes.items():

    for successor in dot_graph.successors(source_node):

        queue = deque([successor])
        visited = set()

        while queue:

            current = queue.popleft()

            if current in visited:
                continue

            visited.add(current)

            if current in processes:

                target_process = (
                    processes[current]
                )

                if (
                    source_process
                    != target_process
                ):
                    dependencies.add(
                        (
                            source_process,
                            target_process
                        )
                    )

                break

            queue.extend(
                dot_graph.successors(
                    current
                )
            )

G = nx.DiGraph()
G.add_edges_from(dependencies)

print("\nDAG METRICS\n")

print(
    f"Nodes               : "
    f"{G.number_of_nodes()}"
)

print(
    f"Edges               : "
    f"{G.number_of_edges()}"
)

roots = [
    n
    for n in G.nodes()
    if G.in_degree(n) == 0
]

leaves = [
    n
    for n in G.nodes()
    if G.out_degree(n) == 0
]

print(
    f"Root nodes          : "
    f"{len(roots)}"
)

print(
    f"Leaf nodes          : "
    f"{len(leaves)}"
)

avg_indegree = (
    sum(
        G.in_degree(n)
        for n in G.nodes()
    )
    / G.number_of_nodes()
)

avg_outdegree = (
    sum(
        G.out_degree(n)
        for n in G.nodes()
    )
    / G.number_of_nodes()
)

print(
    f"Average indegree    : "
    f"{avg_indegree:.2f}"
)

print(
    f"Average outdegree   : "
    f"{avg_outdegree:.2f}"
)

print(
    f"DAG                 : "
    f"{nx.is_directed_acyclic_graph(G)}"
)

print(
    f"Longest path length : "
    f"{len(nx.dag_longest_path(G))}"
)