from fileformats.generic.file import File
from fileformats.medimage.nifti import Nifti1
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.dual_regression import DualRegression
import pytest


@pytest.mark.xfail
def test_dualregression_1():
    task = DualRegression()
    task.inputs.in_files = [Nifti1.sample(seed=0)]
    task.inputs.group_IC_maps_4D = Nifti1.sample(seed=1)
    task.inputs.des_norm = True
    task.inputs.design_file = File.sample(seed=4)
    task.inputs.con_file = File.sample(seed=5)
    task.inputs.out_dir = "output"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_dualregression_2():
    task = DualRegression()
    task.inputs.in_files = [Nifti1.sample(seed=0)]
    task.inputs.group_IC_maps_4D = Nifti1.sample(seed=1)
    task.inputs.des_norm = False
    task.inputs.one_sample_group_mean = True
    task.inputs.n_perm = 10
    task.inputs.out_dir = "my_output_directory"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
