from fileformats.generic.file import File
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.tract_skeleton import TractSkeleton
import pytest


@pytest.mark.xfail
def test_tractskeleton_1():
    task = TractSkeleton()
    task.inputs.in_file = File.sample(seed=0)
    task.inputs.distance_map = File.sample(seed=3)
    task.inputs.search_mask_file = File.sample(seed=4)
    task.inputs.use_cingulum_mask = True
    task.inputs.data_file = File.sample(seed=6)
    task.inputs.alt_data_file = File.sample(seed=7)
    task.inputs.alt_skeleton = File.sample(seed=8)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
