from fileformats.generic.file import File
from fileformats.medimage.nifti import Nifti1
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.prepare_fieldmap import PrepareFieldmap
import pytest


@pytest.mark.xfail
def test_preparefieldmap_1():
    task = PrepareFieldmap()
    task.inputs.scanner = "SIEMENS"
    task.inputs.in_phase = Nifti1.sample(seed=1)
    task.inputs.in_magnitude = Nifti1.sample(seed=2)
    task.inputs.nocheck = False
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_preparefieldmap_2():
    task = PrepareFieldmap()
    task.inputs.in_phase = Nifti1.sample(seed=1)
    task.inputs.in_magnitude = Nifti1.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
