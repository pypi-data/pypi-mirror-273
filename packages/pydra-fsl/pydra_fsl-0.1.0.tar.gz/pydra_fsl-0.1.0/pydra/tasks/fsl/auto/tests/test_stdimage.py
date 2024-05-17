from fileformats.generic.file import File
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.std_image import StdImage
import pytest


@pytest.mark.xfail
def test_stdimage_1():
    task = StdImage()
    task.inputs.dimension = "T"
    task.inputs.in_file = File.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
