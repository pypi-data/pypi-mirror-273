from fileformats.generic.directory import Directory
from fileformats.generic.file import File
from fileformats.medimage.diffusion import Bval
from fileformats.medimage.diffusion import Bvec
from fileformats.medimage.nifti import Nifti1
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.bedpostx5 import BEDPOSTX5
import pytest


@pytest.mark.xfail
def test_bedpostx5_1():
    task = BEDPOSTX5()
    task.inputs.dwi = Nifti1.sample(seed=0)
    task.inputs.mask = Nifti1.sample(seed=1)
    task.inputs.bvecs = Bvec.sample(seed=2)
    task.inputs.bvals = Bval.sample(seed=3)
    task.inputs.logdir = Directory.sample(seed=4)
    task.inputs.n_jumps = 5000
    task.inputs.burn_in = 0
    task.inputs.sample_every = 1
    task.inputs.out_dir = Directory.sample(seed=11)
    task.inputs.grad_dev = File.sample(seed=13)
    task.inputs.burn_in_no_ard = 0
    task.inputs.update_proposal_every = 40
    task.inputs.force_dir = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_bedpostx5_2():
    task = BEDPOSTX5()
    task.inputs.dwi = Nifti1.sample(seed=0)
    task.inputs.mask = Nifti1.sample(seed=1)
    task.inputs.bvecs = Bvec.sample(seed=2)
    task.inputs.bvals = Bval.sample(seed=3)
    task.inputs.n_fibres = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
