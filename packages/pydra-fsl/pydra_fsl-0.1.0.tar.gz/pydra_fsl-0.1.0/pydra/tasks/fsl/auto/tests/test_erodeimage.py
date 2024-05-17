from fileformats.generic.file import File
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.erode_image import ErodeImage
import pytest


@pytest.mark.xfail
def test_erodeimage_1():
    task = ErodeImage()
    task.inputs.minimum_filter = False
    task.inputs.kernel_file = File.sample(seed=3)
    task.inputs.in_file = File.sample(seed=4)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
