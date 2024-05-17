from fileformats.generic.file import File
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.distance_map import DistanceMap
import pytest


@pytest.mark.xfail
def test_distancemap_1():
    task = DistanceMap()
    task.inputs.in_file = File.sample(seed=0)
    task.inputs.mask_file = File.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
