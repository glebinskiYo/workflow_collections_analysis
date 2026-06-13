from pathlib import Path
from wfcommons.wfinstances import NextflowLogsParser

ROOT = Path(__file__).resolve().parent.parent

parser = NextflowLogsParser(
    execution_dir=ROOT / "traces"
)

workflow = parser.build_workflow(
    "ampliseq"
)

workflow.write_json(
    ROOT
    / "data"
    / "ampliseq_wfinstance.json"
)