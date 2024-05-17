from fileformats.generic.file import File
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.prelude import PRELUDE
import pytest


@pytest.mark.xfail
def test_prelude_1():
    task = PRELUDE()
    task.inputs.complex_phase_file = File.sample(seed=0)
    task.inputs.magnitude_file = File.sample(seed=1)
    task.inputs.phase_file = File.sample(seed=2)
    task.inputs.mask_file = File.sample(seed=9)
    task.inputs.savemask_file = File.sample(seed=12)
    task.inputs.rawphase_file = File.sample(seed=13)
    task.inputs.label_file = File.sample(seed=14)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
