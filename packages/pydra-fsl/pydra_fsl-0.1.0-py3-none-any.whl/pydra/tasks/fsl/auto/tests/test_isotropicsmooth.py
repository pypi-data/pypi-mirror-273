from fileformats.generic.file import File
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.isotropic_smooth import IsotropicSmooth
import pytest


@pytest.mark.xfail
def test_isotropicsmooth_1():
    task = IsotropicSmooth()
    task.inputs.in_file = File.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
