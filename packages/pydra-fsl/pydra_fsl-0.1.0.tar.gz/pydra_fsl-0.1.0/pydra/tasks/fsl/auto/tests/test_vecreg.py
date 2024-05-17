from fileformats.datascience.data import TextMatrix
from fileformats.generic.file import File
from fileformats.medimage.nifti import Nifti1
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.vec_reg import VecReg
import pytest


@pytest.mark.xfail
def test_vecreg_1():
    task = VecReg()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.ref_vol = Nifti1.sample(seed=2)
    task.inputs.affine_mat = TextMatrix.sample(seed=3)
    task.inputs.warp_field = File.sample(seed=4)
    task.inputs.rotation_mat = File.sample(seed=5)
    task.inputs.rotation_warp = File.sample(seed=6)
    task.inputs.mask = File.sample(seed=8)
    task.inputs.ref_mask = File.sample(seed=9)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_vecreg_2():
    task = VecReg()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.out_file = "diffusion_vreg.nii"
    task.inputs.ref_vol = Nifti1.sample(seed=2)
    task.inputs.affine_mat = TextMatrix.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
