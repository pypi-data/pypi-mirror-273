from fileformats.generic.file import File
from fileformats.medimage.diffusion import Bval
from fileformats.medimage.diffusion import Bvec
from fileformats.text import TextFile
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.eddy_quad import EddyQuad
import pytest


@pytest.mark.xfail
def test_eddyquad_1():
    task = EddyQuad()
    task.inputs.base_name = "eddy_corrected"
    task.inputs.idx_file = File.sample(seed=1)
    task.inputs.param_file = TextFile.sample(seed=2)
    task.inputs.mask_file = File.sample(seed=3)
    task.inputs.bval_file = Bval.sample(seed=4)
    task.inputs.bvec_file = Bvec.sample(seed=5)
    task.inputs.field = File.sample(seed=7)
    task.inputs.slice_spec = File.sample(seed=8)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_eddyquad_2():
    task = EddyQuad()
    task.inputs.param_file = TextFile.sample(seed=2)
    task.inputs.output_dir = "eddy_corrected.qc"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
