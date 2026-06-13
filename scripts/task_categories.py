import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent

with open(
    ROOT / "data" / "ampliseq_wfinstance.json"
) as f:
    wf = json.load(f)

counter = Counter()

for task in wf["workflow"]["execution"]["tasks"]:
    counter[task["category"]] += 1

results = sorted(
    counter.items(),
    key=lambda x: x[1],
    reverse=True
)

print(
    f"{'CATEGORY':40}"
    f"{'COUNT':>12}"
)

for category, count in results:
    print(
        f"{category:40}"
        f"{count:12}"
    )

print("\nTOP 3 MOST FREQUENT CATEGORIES\n")

for category, count in results[:3]:
    print(
        f"{category:40}"
        f"{count:12}"
    )

counts = [count for _, count in results]

print("\nOVERALL CATEGORY STATISTICS\n")

print(
    f"Maximum count: "
    f"{max(counts)}"
)

print(
    f"Average count across categories: "
    f"{sum(counts) / len(counts):.2f}"
)

print(
    f"Minimum count: "
    f"{min(counts)}"
)