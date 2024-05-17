from fileformats.generic.file import File
from fileformats.medimage.nifti import Nifti1
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.flirt import FLIRT
import pytest


@pytest.mark.xfail
def test_flirt_1():
    task = FLIRT()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.reference = Nifti1.sample(seed=1)
    task.inputs.in_matrix_file = File.sample(seed=5)
    task.inputs.schedule = File.sample(seed=29)
    task.inputs.ref_weight = File.sample(seed=30)
    task.inputs.in_weight = File.sample(seed=31)
    task.inputs.wm_seg = File.sample(seed=38)
    task.inputs.wmcoords = File.sample(seed=39)
    task.inputs.wmnorms = File.sample(seed=40)
    task.inputs.fieldmap = File.sample(seed=41)
    task.inputs.fieldmapmask = File.sample(seed=42)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_flirt_2():
    task = FLIRT()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.reference = Nifti1.sample(seed=1)
    task.inputs.cost_func = "mutualinfo"
    task.inputs.bins = 640
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
