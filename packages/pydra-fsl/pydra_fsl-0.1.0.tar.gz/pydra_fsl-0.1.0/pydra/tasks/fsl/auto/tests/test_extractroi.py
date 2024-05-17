from fileformats.generic.file import File
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.extract_roi import ExtractROI
import pytest


@pytest.mark.xfail
def test_extractroi_1():
    task = ExtractROI()
    task.inputs.in_file = File.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_extractroi_2():
    task = ExtractROI()
    task.inputs.in_file = File.sample(seed=0)
    task.inputs.roi_file = "bar.nii"
    task.inputs.t_min = 0
    task.inputs.t_size = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
