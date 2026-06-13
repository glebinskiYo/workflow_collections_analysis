import json
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent

with open(
    ROOT / "data" / "ampliseq_wfinstance.json"
) as f:
    wf = json.load(f)

runtimes = defaultdict(list)

for task in wf["workflow"]["execution"]["tasks"]:

    runtimes[
        task["category"]
    ].append(
        task["runtimeInSeconds"]
    )

results = []

for category, values in runtimes.items():

    avg_runtime = (
        sum(values)
        / len(values)
    )

    results.append(
        (
            category,
            avg_runtime,
            max(values),
            len(values)
        )
    )

results.sort(
    key=lambda x: x[1],
    reverse=True
)

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

print("\nTOP 3 LONGEST-RUNNING CATEGORIES\n")

for category, avg_runtime, _, _ in results[:3]:

    print(
        f"{category:40}"
        f"{avg_runtime:12.2f} s"
    )

all_avg_runtimes = [
    avg_runtime
    for _, avg_runtime, _, _
    in results
]

print("\nOVERALL RUNTIME STATISTICS\n")

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