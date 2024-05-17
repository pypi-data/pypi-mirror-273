from fileformats.generic.file import File
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.multiple_regress_design import MultipleRegressDesign
import pytest


@pytest.mark.xfail
def test_multipleregressdesign_1():
    task = MultipleRegressDesign()
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
