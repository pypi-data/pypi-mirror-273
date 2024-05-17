from fileformats.generic.file import File
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.proj_thresh import ProjThresh
import pytest


@pytest.mark.xfail
def test_projthresh_1():
    task = ProjThresh()
    task.inputs.in_files = [File.sample(seed=0)]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_projthresh_2():
    task = ProjThresh()
    task.inputs.in_files = [File.sample(seed=0)]
    task.inputs.threshold = 3
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
