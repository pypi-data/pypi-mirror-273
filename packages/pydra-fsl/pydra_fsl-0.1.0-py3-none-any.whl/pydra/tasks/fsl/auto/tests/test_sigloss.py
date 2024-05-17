from fileformats.generic.file import File
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.sig_loss import SigLoss
import pytest


@pytest.mark.xfail
def test_sigloss_1():
    task = SigLoss()
    task.inputs.in_file = File.sample(seed=0)
    task.inputs.mask_file = File.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
