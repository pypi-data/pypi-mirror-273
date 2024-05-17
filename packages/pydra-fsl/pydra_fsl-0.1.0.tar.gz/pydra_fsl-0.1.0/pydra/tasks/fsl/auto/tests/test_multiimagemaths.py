from fileformats.medimage.nifti import Nifti1
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.multi_image_maths import MultiImageMaths
import pytest


@pytest.mark.xfail
def test_multiimagemaths_1():
    task = MultiImageMaths()
    task.inputs.operand_files = [Nifti1.sample(seed=1)]
    task.inputs.in_file = Nifti1.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_multiimagemaths_2():
    task = MultiImageMaths()
    task.inputs.op_string = "-add %s -mul -1 -div %s"
    task.inputs.operand_files = [Nifti1.sample(seed=1)]
    task.inputs.in_file = Nifti1.sample(seed=2)
    task.inputs.out_file = "functional4.nii"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
