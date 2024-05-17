from fileformats.generic.file import File
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.complex import Complex
import pytest


@pytest.mark.xfail
def test_complex_1():
    task = Complex()
    task.inputs.complex_in_file = File.sample(seed=0)
    task.inputs.complex_in_file2 = File.sample(seed=1)
    task.inputs.real_in_file = File.sample(seed=2)
    task.inputs.imaginary_in_file = File.sample(seed=3)
    task.inputs.magnitude_in_file = File.sample(seed=4)
    task.inputs.phase_in_file = File.sample(seed=5)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
