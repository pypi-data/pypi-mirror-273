from fileformats.generic.file import File
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.binary_maths import BinaryMaths
import pytest


@pytest.mark.xfail
def test_binarymaths_1():
    task = BinaryMaths()
    task.inputs.operand_file = File.sample(seed=1)
    task.inputs.in_file = File.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
