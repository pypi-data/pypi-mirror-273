from fileformats.generic.file import File
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.smm import SMM
import pytest


@pytest.mark.xfail
def test_smm_1():
    task = SMM()
    task.inputs.spatial_data_file = File.sample(seed=0)
    task.inputs.mask = File.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
