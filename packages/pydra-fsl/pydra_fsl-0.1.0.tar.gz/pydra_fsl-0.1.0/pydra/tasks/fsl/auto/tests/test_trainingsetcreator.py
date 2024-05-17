from fileformats.generic.directory import Directory
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.training_set_creator import TrainingSetCreator
import pytest


@pytest.mark.xfail
def test_trainingsetcreator_1():
    task = TrainingSetCreator()
    task.inputs.mel_icas_in = [Directory.sample(seed=0)]
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
