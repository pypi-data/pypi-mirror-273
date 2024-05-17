from fileformats.generic.directory import Directory
from fileformats.generic.file import File
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.filmgls import FILMGLS
import pytest


@pytest.mark.xfail
def test_filmgls_1():
    task = FILMGLS()
    task.inputs.in_file = File.sample(seed=0)
    task.inputs.design_file = File.sample(seed=1)
    task.inputs.threshold = 1000.0
    task.inputs.results_dir = "results"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
