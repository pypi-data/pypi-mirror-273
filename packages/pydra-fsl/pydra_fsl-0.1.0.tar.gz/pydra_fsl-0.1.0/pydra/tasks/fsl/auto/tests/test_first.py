from fileformats.generic.file import File
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.first import FIRST
import pytest


@pytest.mark.xfail
def test_first_1():
    task = FIRST()
    task.inputs.in_file = File.sample(seed=0)
    task.inputs.method = "auto"
    task.inputs.affine_file = File.sample(seed=8)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
