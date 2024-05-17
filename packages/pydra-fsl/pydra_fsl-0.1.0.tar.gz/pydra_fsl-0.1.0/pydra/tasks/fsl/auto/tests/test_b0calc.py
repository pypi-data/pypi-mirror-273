from fileformats.medimage.nifti import Nifti1
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.b0_calc import B0Calc
import pytest


@pytest.mark.xfail
def test_b0calc_1():
    task = B0Calc()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.x_grad = 0.0
    task.inputs.y_grad = 0.0
    task.inputs.z_grad = 0.0
    task.inputs.x_b0 = 0.0
    task.inputs.y_b0 = 0.0
    task.inputs.z_b0 = 1.0
    task.inputs.delta = -9.45e-06
    task.inputs.chi_air = 4e-07
    task.inputs.compute_xyz = False
    task.inputs.extendboundary = 1.0
    task.inputs.directconv = False
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_b0calc_2():
    task = B0Calc()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.z_b0 = 3.0
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
