from fileformats.generic.file import File
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.apply_xfm import ApplyXFM
import pytest


@pytest.mark.xfail
def test_applyxfm_1():
    task = ApplyXFM()
    task.inputs.apply_xfm = True
    task.inputs.in_file = File.sample(seed=1)
    task.inputs.reference = File.sample(seed=2)
    task.inputs.in_matrix_file = File.sample(seed=6)
    task.inputs.schedule = File.sample(seed=29)
    task.inputs.ref_weight = File.sample(seed=30)
    task.inputs.in_weight = File.sample(seed=31)
    task.inputs.wm_seg = File.sample(seed=38)
    task.inputs.wmcoords = File.sample(seed=39)
    task.inputs.wmnorms = File.sample(seed=40)
    task.inputs.fieldmap = File.sample(seed=41)
    task.inputs.fieldmapmask = File.sample(seed=42)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
