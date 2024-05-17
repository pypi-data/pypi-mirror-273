from fileformats.generic.file import File
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.image_maths import ImageMaths
import pytest


@pytest.mark.xfail
def test_imagemaths_1():
    task = ImageMaths()
    task.inputs.in_file = File.sample(seed=0)
    task.inputs.in_file2 = File.sample(seed=1)
    task.inputs.mask_file = File.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_imagemaths_2():
    task = ImageMaths()
    task.inputs.in_file = File.sample(seed=0)
    task.inputs.out_file = "foo_maths.nii"
    task.inputs.op_string = "-add 5"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
