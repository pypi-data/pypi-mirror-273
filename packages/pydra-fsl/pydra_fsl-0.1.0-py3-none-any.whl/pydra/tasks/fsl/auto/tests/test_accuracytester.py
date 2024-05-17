from fileformats.generic.directory import Directory
from fileformats.generic.file import File
from fileformats.medimage_fsl import MelodicIca
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.accuracy_tester import AccuracyTester
import pytest


@pytest.mark.xfail
def test_accuracytester_1():
    task = AccuracyTester()
    task.inputs.mel_icas = [MelodicIca.sample(seed=0)]
    task.inputs.trained_wts_file = File.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
