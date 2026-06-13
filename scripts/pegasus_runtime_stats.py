import json
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent

with open(
    ROOT
    / "data"
    / "epigenomics-chameleon-hep-2seq-100k-001.json"
) as f:
    wf = json.load(f)

runtimes = defaultdict(list)

# Execution tasks live here, same as in ampliseq
for task in wf["workflow"]["execution"]["tasks"]:
    # Pegasus instance has no "category" field.
    # Use the program name as the category (e.g. "fast2bfq", "map", "filterContams").
    program = task["command"]["program"]
    runtimes[program].append(task["runtimeInSeconds"])

results = []

for category, values in runtimes.items():
    avg_runtime = sum(values) / len(values)
    results.append(
        (
            category,
            avg_runtime,
            max(values),
            len(values),
        )
    )

# highest average runtime first
results.sort(key=lambda x: x[1], reverse=True)

print(
    f"{'CATEGORY':40}"
    f"{'AVG':>12}"
    f"{'MAX':>12}"
    f"{'COUNT':>12}"
)

for category, avg_runtime, max_runtime, count in results:
    print(
        f"{category:40}"
        f"{avg_runtime:12.2f}"
        f"{max_runtime:12.2f}"
        f"{count:12}"
    )

print("\nTOP 3 LONGEST-RUNNING TASKS")

for category, avg_runtime, max_runtime, count in results[:3]:
    print(
        f"{category:40}"
        f"{avg_runtime:12.2f} s"
    )

all_avg_runtimes = [
    avg_runtime
    for _, avg_runtime, _, _
    in results
]

print("\nOVERALL RUNTIME STATISTICS")

print(
    f"Maximum average runtime: "
    f"{max(all_avg_runtimes):.2f} s"
)

print(
    f"Average runtime across categories: "
    f"{sum(all_avg_runtimes) / len(all_avg_runtimes):.2f} s"
)

print(
    f"Minimum average runtime: "
    f"{min(all_avg_runtimes):.2f} s"
)

# Execution tasks live here, same as in ampliseq
for task in wf["workflow"]["execution"]["tasks"]:
    # Pegasus instance has no "category" field.
    # Use the program name as the category (e.g. "fast2bfq", "map", "filterContams").
    program = task["command"]["program"]
    runtimes[program].append(task["runtimeInSeconds"])

results = []

for category, values in runtimes.items():
    avg_runtime = sum(values) / len(values)
    results.append(
        (
            category,
            avg_runtime,
            max(values),
            len(values),
        )
    )

# highest average runtime first
results.sort(key=lambda x: x[1], reverse=True)

print(
    f"{'CATEGORY':40}"
    f"{'AVG':>12}"
    f"{'MAX':>12}"
    f"{'COUNT':>12}"
)

for category, avg_runtime, max_runtime, count in results:
    print(
        f"{category:40}"
        f"{avg_runtime:12.2f}"
        f"{max_runtime:12.2f}"
        f"{count:12}"
    )

print("\nTOP 3 LONGEST-RUNNING TASKS")

for category, avg_runtime, max_runtime, count in results[:3]:
    print(
        f"{category:40}"
        f"{avg_runtime:12.2f} s"
    )

all_avg_runtimes = [
    avg_runtime
    for _, avg_runtime, _, _
    in results
]

print("\nOVERALL RUNTIME STATISTICS")

print(
    f"Maximum average runtime: "
    f"{max(all_avg_runtimes):.2f} s"
)

print(
    f"Average runtime across categories: "
    f"{sum(all_avg_runtimes) / len(all_avg_runtimes):.2f} s"
)

print(
    f"Minimum average runtime: "
    f"{min(all_avg_runtimes):.2f} s"
)