from fileformats.medimage.nifti import Nifti1
from fileformats.medimage.nifti import NiftiGz
from fileformats.text import TextFile
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.apply_topup import ApplyTOPUP
import pytest


@pytest.mark.xfail
def test_applytopup_1():
    task = ApplyTOPUP()
    task.inputs.in_files = [Nifti1.sample(seed=0)]
    task.inputs.encoding_file = TextFile.sample(seed=1)
    task.inputs.in_topup_fieldcoef = NiftiGz.sample(seed=3)
    task.inputs.in_topup_movpar = TextFile.sample(seed=4)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_applytopup_2():
    task = ApplyTOPUP()
    task.inputs.in_files = [Nifti1.sample(seed=0)]
    task.inputs.encoding_file = TextFile.sample(seed=1)
    task.inputs.in_topup_fieldcoef = NiftiGz.sample(seed=3)
    task.inputs.in_topup_movpar = TextFile.sample(seed=4)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
