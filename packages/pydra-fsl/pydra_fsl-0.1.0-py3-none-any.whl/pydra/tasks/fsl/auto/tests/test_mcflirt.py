from fileformats.generic.file import File
from fileformats.medimage.nifti import Nifti1
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.mcflirt import MCFLIRT
import pytest


@pytest.mark.xfail
def test_mcflirt_1():
    task = MCFLIRT()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.init = File.sample(seed=10)
    task.inputs.ref_file = File.sample(seed=19)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_mcflirt_2():
    task = MCFLIRT()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.out_file = "moco.nii"
    task.inputs.cost = "mutualinfo"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
