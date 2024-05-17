from fileformats.generic.file import File
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.image_meants import ImageMeants
import pytest


@pytest.mark.xfail
def test_imagemeants_1():
    task = ImageMeants()
    task.inputs.in_file = File.sample(seed=0)
    task.inputs.mask = File.sample(seed=2)
    task.inputs.order = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
