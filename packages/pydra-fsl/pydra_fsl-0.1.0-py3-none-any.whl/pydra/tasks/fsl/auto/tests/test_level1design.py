from fileformats.generic.file import File
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.engine.specs import MultiOutputType
from pydra.tasks.fsl.auto.level_1_design import Level1Design
import pytest


@pytest.mark.xfail
def test_level1design_1():
    task = Level1Design()
    task.inputs.orthogonalization = {}
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
