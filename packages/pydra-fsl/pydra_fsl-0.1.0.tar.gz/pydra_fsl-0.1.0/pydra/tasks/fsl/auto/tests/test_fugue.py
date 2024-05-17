from fileformats.generic.file import File
from fileformats.medimage.nifti import Nifti1
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.fugue import FUGUE
import pytest


@pytest.mark.xfail
def test_fugue_1():
    task = FUGUE()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.shift_in_file = Nifti1.sample(seed=1)
    task.inputs.phasemap_in_file = Nifti1.sample(seed=2)
    task.inputs.fmap_in_file = File.sample(seed=3)
    task.inputs.forward_warping = False
    task.inputs.mask_file = Nifti1.sample(seed=24)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_fugue_2():
    task = FUGUE()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.shift_in_file = Nifti1.sample(seed=1)
    task.inputs.unwarp_direction = "y"
    task.inputs.mask_file = Nifti1.sample(seed=24)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_fugue_3():
    task = FUGUE()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.shift_in_file = Nifti1.sample(seed=1)
    task.inputs.forward_warping = True
    task.inputs.unwarp_direction = "y"
    task.inputs.mask_file = Nifti1.sample(seed=24)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_fugue_4():
    task = FUGUE()
    task.inputs.phasemap_in_file = Nifti1.sample(seed=2)
    task.inputs.dwell_to_asym_ratio = (0.77e-3 * 3) / 2.46e-3
    task.inputs.unwarp_direction = "y"
    task.inputs.mask_file = Nifti1.sample(seed=24)
    task.inputs.save_shift = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
