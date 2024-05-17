from fileformats.generic.file import File
from fileformats.medimage.nifti import Nifti1
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.motion_outliers import MotionOutliers
import pytest


@pytest.mark.xfail
def test_motionoutliers_1():
    task = MotionOutliers()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.mask = File.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_motionoutliers_2():
    task = MotionOutliers()
    task.inputs.in_file = Nifti1.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
