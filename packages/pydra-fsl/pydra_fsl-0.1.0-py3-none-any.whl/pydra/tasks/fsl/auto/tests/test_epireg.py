from fileformats.generic.file import File
from fileformats.medimage.nifti import Nifti1
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.epi_reg import EpiReg
import pytest


@pytest.mark.xfail
def test_epireg_1():
    task = EpiReg()
    task.inputs.epi = Nifti1.sample(seed=0)
    task.inputs.t1_head = Nifti1.sample(seed=1)
    task.inputs.t1_brain = Nifti1.sample(seed=2)
    task.inputs.out_base = "epi2struct"
    task.inputs.fmap = Nifti1.sample(seed=4)
    task.inputs.fmapmag = Nifti1.sample(seed=5)
    task.inputs.fmapmagbrain = Nifti1.sample(seed=6)
    task.inputs.weight_image = File.sample(seed=10)
    task.inputs.no_clean = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_epireg_2():
    task = EpiReg()
    task.inputs.epi = Nifti1.sample(seed=0)
    task.inputs.t1_head = Nifti1.sample(seed=1)
    task.inputs.t1_brain = Nifti1.sample(seed=2)
    task.inputs.out_base = "epi2struct"
    task.inputs.fmap = Nifti1.sample(seed=4)
    task.inputs.fmapmag = Nifti1.sample(seed=5)
    task.inputs.fmapmagbrain = Nifti1.sample(seed=6)
    task.inputs.echospacing = 0.00067
    task.inputs.pedir = "y"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
