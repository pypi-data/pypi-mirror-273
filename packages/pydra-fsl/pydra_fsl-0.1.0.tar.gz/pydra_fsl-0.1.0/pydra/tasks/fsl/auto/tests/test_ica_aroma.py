from fileformats.datascience.data import TextMatrix
from fileformats.generic.directory import Directory
from fileformats.generic.file import File
from fileformats.medimage.nifti import Nifti1
from fileformats.medimage.nifti import NiftiGz
from fileformats.text import TextFile
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.ica__aroma import ICA_AROMA
import pytest


@pytest.mark.xfail
def test_ica_aroma_1():
    task = ICA_AROMA()
    task.inputs.feat_dir = Directory.sample(seed=0)
    task.inputs.in_file = Nifti1.sample(seed=1)
    task.inputs.mask = NiftiGz.sample(seed=3)
    task.inputs.melodic_dir = Directory.sample(seed=6)
    task.inputs.mat_file = TextMatrix.sample(seed=7)
    task.inputs.fnirt_warp_file = Nifti1.sample(seed=8)
    task.inputs.motion_parameters = TextFile.sample(seed=9)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_ica_aroma_2():
    task = ICA_AROMA()
    task.inputs.in_file = Nifti1.sample(seed=1)
    task.inputs.out_dir = "ICA_testout"
    task.inputs.mask = NiftiGz.sample(seed=3)
    task.inputs.mat_file = TextMatrix.sample(seed=7)
    task.inputs.fnirt_warp_file = Nifti1.sample(seed=8)
    task.inputs.motion_parameters = TextFile.sample(seed=9)
    task.inputs.denoise_type = "both"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
