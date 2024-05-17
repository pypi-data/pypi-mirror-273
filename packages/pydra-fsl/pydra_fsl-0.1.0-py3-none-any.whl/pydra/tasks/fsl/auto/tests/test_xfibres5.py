from fileformats.generic.directory import Directory
from fileformats.generic.file import File
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.x_fibres_5 import XFibres5
import pytest


@pytest.mark.xfail
def test_xfibres5_1():
    task = XFibres5()
    task.inputs.gradnonlin = File.sample(seed=0)
    task.inputs.dwi = File.sample(seed=1)
    task.inputs.mask = File.sample(seed=2)
    task.inputs.bvecs = File.sample(seed=3)
    task.inputs.bvals = File.sample(seed=4)
    task.inputs.logdir = Directory.sample(seed=5)
    task.inputs.n_jumps = 5000
    task.inputs.burn_in = 0
    task.inputs.burn_in_no_ard = 0
    task.inputs.sample_every = 1
    task.inputs.update_proposal_every = 40
    task.inputs.force_dir = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
