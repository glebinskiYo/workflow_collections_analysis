# Reproducing the Workflow Analysis

## Requirements

The following software must be installed:

* Java (required by Nextflow)
* Nextflow
* Python 3.10+
* Git
* Docker

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

## Quick Start

The repository already contains:

```text
ampliseq_wfinstance.json
ampliseq.dot
epigenomics-chameleon-hep-2seq-100k-001.json
```

If the goal is only to reproduce the analyses presented in the paper, executing a new workflow is not required. Simply clone the repository, install the required Python dependencies, and run the analysis scripts:

```bash
git clone https://github.com/glebinskiYo/workflow_collections_analysis.git
cd workflow_collections_analysis

pip install wfcommons networkx pydot matplotlib
```

Example:

```bash
python scripts/nextflow_dag_metrics.py
python scripts/task_categories.py
python scripts/nextflow_runtime_stats.py
python scripts/nextflow_resource_stats.py
```

The workflow execution and WfInstance generation steps described below are only necessary when generating a new WfInstance from a different nf-core workflow execution.


## Executing an nf-core Workflow

Create a new directory:

```bash
mkdir ampliseq_execution
cd ampliseq_execution
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

Export the DAG as a DOT file:

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

The repository is configured for the workflow instance and DAG included with this project. When analyzing a different workflow, the workflow must first be executed with Nextflow monitoring enabled to generate the required execution artifacts:

```text
trace.txt
execution_report_<workflow>.html
execution_timeline_<workflow>.html
dag.html
```

These files can then be used to generate a new WfInstance and DAG representation.

The WfInstance generation script must be updated wherever the workflow name or output filename is specified. For example:

```python
workflow = parser.build_workflow(
    "<workflow_name>"
)
```

and

```python
workflow.write_json(
    ROOT
    / "data"
    / "<workflow_name>_wfinstance.json"
)
```

must be replaced with values corresponding to the new workflow.

Similarly, the analysis scripts currently reference:

```python
ROOT / "data" / "ampliseq_wfinstance.json"
```

and

```python
ROOT / "data" / "ampliseq.dot"
```

These paths must be updated to point to the WfInstance JSON file and DOT file generated for the new workflow.

In general, every occurrence of the original workflow name within file paths, input filenames, output filenames, and workflow identifiers must be replaced with the corresponding values of the new workflow. Once these changes have been made, the analysis scripts can be executed without further modification, provided that the generated workflow instance conforms to the WfCommons WfFormat schema.

