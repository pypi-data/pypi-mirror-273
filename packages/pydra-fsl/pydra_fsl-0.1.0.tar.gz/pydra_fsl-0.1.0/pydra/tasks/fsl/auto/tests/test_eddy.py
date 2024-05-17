from fileformats.generic.file import File
from fileformats.medimage.diffusion import Bval
from fileformats.medimage.diffusion import Bvec
from fileformats.medimage.nifti import Nifti1
from fileformats.text import TextFile
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.eddy import Eddy
import pytest


@pytest.mark.xfail
def test_eddy_1():
    task = Eddy()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.in_mask = File.sample(seed=1)
    task.inputs.in_index = TextFile.sample(seed=2)
    task.inputs.in_acqp = File.sample(seed=3)
    task.inputs.in_bvec = Bvec.sample(seed=4)
    task.inputs.in_bval = Bval.sample(seed=5)
    task.inputs.out_base = "eddy_corrected"
    task.inputs.session = File.sample(seed=7)
    task.inputs.in_topup_fieldcoef = File.sample(seed=8)
    task.inputs.in_topup_movpar = File.sample(seed=9)
    task.inputs.field = File.sample(seed=10)
    task.inputs.field_mat = File.sample(seed=11)
    task.inputs.flm = "quadratic"
    task.inputs.slm = "none"
    task.inputs.interp = "spline"
    task.inputs.nvoxhp = 1000
    task.inputs.fudge_factor = 10.0
    task.inputs.niter = 5
    task.inputs.method = "jac"
    task.inputs.slice_order = TextFile.sample(seed=36)
    task.inputs.json = File.sample(seed=37)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_eddy_2():
    task = Eddy()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.in_index = TextFile.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_eddy_3():
    task = Eddy()
    task.inputs.use_cuda = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_eddy_4():
    task = Eddy()
    task.inputs.mporder = 6
    task.inputs.slice2vol_niter = 5
    task.inputs.slice2vol_lambda = 1
    task.inputs.slice2vol_interp = "trilinear"
    task.inputs.slice_order = TextFile.sample(seed=36)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
