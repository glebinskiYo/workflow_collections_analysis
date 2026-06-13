import json
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent

with open(
    ROOT / "data" / "ampliseq_wfinstance.json"
) as f:
    wf = json.load(f)

memory = defaultdict(list)

for task in wf["workflow"]["execution"]["tasks"]:

    memory[
        task["category"]
    ].append(
        task["memoryInBytes"]
    )

results = []

for category, values in memory.items():

    avg_mb = (
        sum(values)
        / len(values)
    ) / 1024 / 1024

    results.append(
        (
            category,
            avg_mb
        )
    )

results.sort(
    key=lambda x: x[1],
    reverse=True
)

print(
    f"{'CATEGORY':40}"
    f"{'AVG MEMORY (MB)':>20}"
)

for category, avg_mb in results:

    print(
        f"{category:40}"
        f"{avg_mb:20.2f}"
    )

print("\nTOP 3 MOST MEMORY-INTENSIVE CATEGORIES\n")

for category, avg_mb in results[:3]:

    print(
        f"{category:40}"
        f"{avg_mb:20.2f}"
    )

all_avg_memory = [
    avg_mb
    for _, avg_mb
    in results
]

print("\nOVERALL MEMORY STATISTICS\n")

print(
    f"Maximum average memory: "
    f"{max(all_avg_memory):.2f} MB"
)

print(
    f"Average memory across categories: "
    f"{sum(all_avg_memory) / len(all_avg_memory):.2f} MB"
)

print(
    f"Minimum average memory: "
    f"{min(all_avg_memory):.2f} MB"
)