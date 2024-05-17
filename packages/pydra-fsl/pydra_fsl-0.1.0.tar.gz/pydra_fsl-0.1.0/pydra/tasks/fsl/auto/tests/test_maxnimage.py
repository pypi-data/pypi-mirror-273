from fileformats.generic.file import File
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.maxn_image import MaxnImage
import pytest


@pytest.mark.xfail
def test_maxnimage_1():
    task = MaxnImage()
    task.inputs.dimension = "T"
    task.inputs.in_file = File.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
