from fileformats.generic.file import File
from fileformats.medimage.nifti import Nifti1
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.convert_warp import ConvertWarp
import pytest


@pytest.mark.xfail
def test_convertwarp_1():
    task = ConvertWarp()
    task.inputs.reference = Nifti1.sample(seed=0)
    task.inputs.premat = File.sample(seed=2)
    task.inputs.warp1 = Nifti1.sample(seed=3)
    task.inputs.midmat = File.sample(seed=4)
    task.inputs.warp2 = File.sample(seed=5)
    task.inputs.postmat = File.sample(seed=6)
    task.inputs.shift_in_file = File.sample(seed=7)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_convertwarp_2():
    task = ConvertWarp()
    task.inputs.reference = Nifti1.sample(seed=0)
    task.inputs.warp1 = Nifti1.sample(seed=3)
    task.inputs.relwarp = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
