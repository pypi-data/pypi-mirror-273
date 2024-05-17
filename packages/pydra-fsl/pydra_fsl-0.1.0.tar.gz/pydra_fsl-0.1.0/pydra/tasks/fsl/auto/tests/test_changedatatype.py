from fileformats.generic.file import File
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.change_data_type import ChangeDataType
import pytest


@pytest.mark.xfail
def test_changedatatype_1():
    task = ChangeDataType()
    task.inputs.in_file = File.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
