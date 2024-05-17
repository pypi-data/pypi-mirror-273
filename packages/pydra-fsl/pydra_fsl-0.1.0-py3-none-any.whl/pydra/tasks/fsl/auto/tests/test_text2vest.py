from fileformats.datascience.data import TextMatrix
from fileformats.text import TextFile
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.text_2_vest import Text2Vest
import pytest


@pytest.mark.xfail
def test_text2vest_1():
    task = Text2Vest()
    task.inputs.in_file = TextFile.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_text2vest_2():
    task = Text2Vest()
    task.inputs.in_file = TextFile.sample(seed=0)
    task.inputs.out_file = "design.mat"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
