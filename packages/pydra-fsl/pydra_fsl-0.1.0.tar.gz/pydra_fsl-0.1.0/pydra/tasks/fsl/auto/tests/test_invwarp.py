from fileformats.medimage.nifti import Nifti1
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.inv_warp import InvWarp
import pytest


@pytest.mark.xfail
def test_invwarp_1():
    task = InvWarp()
    task.inputs.warp = Nifti1.sample(seed=0)
    task.inputs.reference = Nifti1.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_invwarp_2():
    task = InvWarp()
    task.inputs.warp = Nifti1.sample(seed=0)
    task.inputs.reference = Nifti1.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
