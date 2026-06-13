import json
from pathlib import Path
import networkx as nx

ROOT = Path(__file__).resolve().parent.parent

with open(
    ROOT
    / "data"
    / "epigenomics-chameleon-hep-2seq-100k-001.json"
) as f:
    wf = json.load(f)

G = nx.DiGraph()

tasks = wf["workflow"]["specification"]["tasks"]

for task in tasks:

    task_id = task["id"]

    G.add_node(task_id)

    for parent in task.get("parents", []):

        G.add_edge(
            parent,
            task_id
        )

print("\nDAG METRICS\n")

print(f"Nodes               : {G.number_of_nodes()}")
print(f"Edges               : {G.number_of_edges()}")

roots = [
    n for n in G.nodes()
    if G.in_degree(n) == 0
]

leaves = [
    n for n in G.nodes()
    if G.out_degree(n) == 0
]

print(f"Root nodes          : {len(roots)}")
print(f"Leaf nodes          : {len(leaves)}")

print(
    f"Average indegree    : "
    f"{sum(G.in_degree(n) for n in G.nodes()) / G.number_of_nodes():.2f}"
)

print(
    f"Average outdegree   : "
    f"{sum(G.out_degree(n) for n in G.nodes()) / G.number_of_nodes():.2f}"
)

print(
    f"DAG                 : "
    f"{nx.is_directed_acyclic_graph(G)}"
)

print(
    f"Longest path length : "
    f"{len(nx.dag_longest_path(G))}"
)