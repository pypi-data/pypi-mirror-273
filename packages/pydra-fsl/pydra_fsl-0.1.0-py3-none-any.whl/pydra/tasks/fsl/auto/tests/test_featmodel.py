from fileformats.generic.file import File
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.feat_model import FEATModel
import pytest


@pytest.mark.xfail
def test_featmodel_1():
    task = FEATModel()
    task.inputs.fsf_file = File.sample(seed=0)
    task.inputs.ev_files = [File.sample(seed=1)]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
