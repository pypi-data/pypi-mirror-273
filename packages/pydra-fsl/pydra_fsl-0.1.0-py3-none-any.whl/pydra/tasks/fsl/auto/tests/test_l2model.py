from fileformats.generic.file import File
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.l2_model import L2Model
import pytest


@pytest.mark.xfail
def test_l2model_1():
    task = L2Model()
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
