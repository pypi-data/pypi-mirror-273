from fileformats.generic.file import File
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.overlay import Overlay
import pytest


@pytest.mark.xfail
def test_overlay_1():
    task = Overlay()
    task.inputs.transparency = True
    task.inputs.out_type = "float"
    task.inputs.background_image = File.sample(seed=3)
    task.inputs.stat_image = File.sample(seed=7)
    task.inputs.stat_image2 = File.sample(seed=10)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
