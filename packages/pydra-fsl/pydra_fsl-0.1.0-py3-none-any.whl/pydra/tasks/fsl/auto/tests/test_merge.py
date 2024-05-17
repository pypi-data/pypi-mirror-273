from fileformats.medimage.nifti import Nifti1
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.merge import Merge
import pytest


@pytest.mark.xfail
def test_merge_1():
    task = Merge()
    task.inputs.in_files = [Nifti1.sample(seed=0)]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_merge_2():
    task = Merge()
    task.inputs.in_files = [Nifti1.sample(seed=0)]
    task.inputs.dimension = "t"
    task.inputs.tr = 2.25
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
