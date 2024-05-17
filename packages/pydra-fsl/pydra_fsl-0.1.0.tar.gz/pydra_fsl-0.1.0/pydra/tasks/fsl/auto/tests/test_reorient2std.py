from fileformats.generic.file import File
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.reorient_2_std import Reorient2Std
import pytest


@pytest.mark.xfail
def test_reorient2std_1():
    task = Reorient2Std()
    task.inputs.in_file = File.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
