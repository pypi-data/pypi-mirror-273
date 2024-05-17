from fileformats.generic.file import File
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.filter_regressor import FilterRegressor
import pytest


@pytest.mark.xfail
def test_filterregressor_1():
    task = FilterRegressor()
    task.inputs.in_file = File.sample(seed=0)
    task.inputs.design_file = File.sample(seed=2)
    task.inputs.mask = File.sample(seed=5)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
