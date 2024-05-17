from fileformats.generic.file import File
from fileformats.medimage.nifti import Nifti1
from fileformats.text import TextFile
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.topup import TOPUP
import pytest


@pytest.mark.xfail
def test_topup_1():
    task = TOPUP()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.encoding_file = TextFile.sample(seed=1)
    task.inputs.readout_times = [File.sample(seed=3)]
    task.inputs.out_warp_prefix = "warpfield"
    task.inputs.out_mat_prefix = "xfm"
    task.inputs.out_jac_prefix = "jac"
    task.inputs.config = "b02b0.cnf"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_topup_2():
    task = TOPUP()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.encoding_file = TextFile.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
