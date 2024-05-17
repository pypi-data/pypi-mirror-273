from fileformats.generic.directory import Directory
from fileformats.generic.file import File
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.feat import FEAT
import pytest


@pytest.mark.xfail
def test_feat_1():
    task = FEAT()
    task.inputs.fsf_file = File.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
