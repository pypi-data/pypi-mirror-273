from fileformats.generic.file import File
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.image_stats import ImageStats
import pytest


@pytest.mark.xfail
def test_imagestats_1():
    task = ImageStats()
    task.inputs.in_file = File.sample(seed=1)
    task.inputs.mask_file = File.sample(seed=3)
    task.inputs.index_mask_file = File.sample(seed=4)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_imagestats_2():
    task = ImageStats()
    task.inputs.in_file = File.sample(seed=1)
    task.inputs.op_string = "-M"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
