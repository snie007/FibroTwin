from __future__ import annotations

from pathlib import Path

from .truth import HodgkinHuxleyTruth
from .experiment import ExperimentSession
from .labbook import LabBook
from .baseline_agent import BaselineAgent


def main(root: Path | None = None) -> None:
    root = root or Path.cwd()
    truth = HodgkinHuxleyTruth()
    session = ExperimentSession(truth=truth, root=root)
    labbook = LabBook(root=root)
    agent = BaselineAgent(session=session, labbook=labbook)
    agent.run()
    print(f"Lab book created at {labbook.output_dir}")


if __name__ == '__main__':
    main()
