from fileformats.generic.file import File
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.slicer import Slicer
import pytest


@pytest.mark.xfail
def test_slicer_1():
    task = Slicer()
    task.inputs.in_file = File.sample(seed=0)
    task.inputs.image_edges = File.sample(seed=1)
    task.inputs.label_slices = True
    task.inputs.colour_map = File.sample(seed=3)
    task.inputs.show_orientation = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
