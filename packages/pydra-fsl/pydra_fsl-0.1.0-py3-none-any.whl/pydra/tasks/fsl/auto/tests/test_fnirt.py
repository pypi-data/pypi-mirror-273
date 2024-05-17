from fileformats.generic.file import File
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.fnirt import FNIRT
import pytest


@pytest.mark.xfail
def test_fnirt_1():
    task = FNIRT()
    task.inputs.ref_file = File.sample(seed=0)
    task.inputs.in_file = File.sample(seed=1)
    task.inputs.affine_file = File.sample(seed=2)
    task.inputs.inwarp_file = File.sample(seed=3)
    task.inputs.in_intensitymap_file = [File.sample(seed=4)]
    task.inputs.refmask_file = File.sample(seed=13)
    task.inputs.inmask_file = File.sample(seed=14)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_fnirt_2():
    task = FNIRT()
    task.inputs.subsampling_scheme = [4, 2, 1, 1]
    task.inputs.warp_resolution = (6, 6, 6)
    task.inputs.in_fwhm = [8, 4, 2, 2]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
