# Reproducing the Workflow Analysis

## Requirements

The following software must be installed:

* Java (required by Nextflow)
* Nextflow
* Python 3.10+
* Git

Python packages:

```bash
pip install wfcommons networkx pydot matplotlib
```

Optional:

```bash
brew install graphviz
```

(Graphviz is required for handling DOT workflow graphs.)

---

## Executing an nf-core Workflow

Create a new directory:

```bash
mkdir ampliseq_execution
cd ampliseq_execution
```

Clone the workflow:

```bash
git clone https://github.com/nf-core/ampliseq.git
cd ampliseq
```

Run the workflow with monitoring enabled:

```bash
nextflow run nf-core/ampliseq \
    -profile docker \
    --input samplesheet.csv \
    --outdir results \
    -with-report execution_report_ampliseq.html \
    -with-timeline execution_timeline_ampliseq.html \
    -with-dag dag.html \
    -with-trace trace.txt
```

After execution, the following artifacts should be available:

```text
trace.txt
execution_report_ampliseq.html
execution_timeline_ampliseq.html
dag.html
```

Export the DAG as a DOT file if required:

```bash
dot -Tdot dag.html > ampliseq.dot
```

---

## Generating a WfInstance

The repository contains:

```text
scripts/generate_wfinstance.py
```

The script expects the execution traces to be stored in:

```text
traces/
```

Repository structure:

```text
workflow_collections_analysis/
│
├── traces/
│   ├── trace.txt
│   ├── execution_report_ampliseq.html
│   └── execution_timeline_ampliseq.html
│
├── data/
│
└── scripts/
```

Generate the workflow instance:

```bash
python scripts/generate_wfinstance.py
```

This creates:

```text
data/ampliseq_wfinstance.json
```

---

## Running the Analysis Scripts

### Nextflow DAG Metrics

```bash
python scripts/nextflow_dag_metrics.py
```

Outputs:

* Node count
* Edge count
* Root nodes
* Leaf nodes
* Average degree
* Longest path length

---

### Task Categories

```bash
python scripts/task_categories.py
```

Outputs:

* Category frequencies
* Top three categories
* Category statistics

---

### Runtime Statistics

```bash
python scripts/nextflow_runtime_stats.py
```

Outputs:

* Average runtime per category
* Maximum runtime per category
* Top three longest-running categories
* Runtime summary statistics

---

### Memory Statistics

```bash
python scripts/nextflow_resource_stats.py
```

Outputs:

* Average memory usage per category
* Top three most memory-intensive categories
* Memory summary statistics

---

### Pegasus Workflow Metrics

```bash
python scripts/pegasus_dag_metrics.py
python scripts/pegasus_runtime_stats.py
```

These scripts analyze the provided Pegasus epigenomics WfInstance:

```text
data/epigenomics-chameleon-hep-2seq-100k-001.json
```

---

## Using a Different Workflow

The analysis scripts currently reference:

```python
ROOT / "data" / "ampliseq_wfinstance.json"
```

If a different workflow instance is generated, replace the filename accordingly.

Example:

```python
with open(
    ROOT / "data" / "rnaseq_wfinstance.json"
) as f:
```

Similarly, DAG scripts reference:

```python
ROOT / "data" / "ampliseq.dot"
```

For another workflow, change this to:

```python
ROOT / "data" / "rnaseq.dot"
```

No further modifications are required as long as the workflow instance conforms to the WfCommons WfFormat schema.
