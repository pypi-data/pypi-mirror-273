from fileformats.datascience.data import TextMatrix
from fileformats.generic.file import File
from fileformats.medimage.nifti import Nifti1
from fileformats.medimage_fsl import Con
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.melodic import MELODIC
import pytest


@pytest.mark.xfail
def test_melodic_1():
    task = MELODIC()
    task.inputs.in_files = [Nifti1.sample(seed=0)]
    task.inputs.mask = File.sample(seed=2)
    task.inputs.ICs = File.sample(seed=27)
    task.inputs.mix = File.sample(seed=28)
    task.inputs.smode = File.sample(seed=29)
    task.inputs.bg_image = File.sample(seed=32)
    task.inputs.t_des = TextMatrix.sample(seed=35)
    task.inputs.t_con = Con.sample(seed=36)
    task.inputs.s_des = TextMatrix.sample(seed=37)
    task.inputs.s_con = Con.sample(seed=38)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_melodic_2():
    task = MELODIC()
    task.inputs.in_files = [Nifti1.sample(seed=0)]
    task.inputs.out_dir = "groupICA.out"
    task.inputs.no_bet = True
    task.inputs.bg_threshold = 10
    task.inputs.approach = "tica"
    task.inputs.mm_thresh = 0.5
    task.inputs.tr_sec = 1.5
    task.inputs.t_des = TextMatrix.sample(seed=35)
    task.inputs.t_con = Con.sample(seed=36)
    task.inputs.s_des = TextMatrix.sample(seed=37)
    task.inputs.s_con = Con.sample(seed=38)
    task.inputs.out_stats = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
