from fileformats.generic.file import File
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.make_dyadic_vectors import MakeDyadicVectors
import pytest


@pytest.mark.xfail
def test_makedyadicvectors_1():
    task = MakeDyadicVectors()
    task.inputs.theta_vol = File.sample(seed=0)
    task.inputs.phi_vol = File.sample(seed=1)
    task.inputs.mask = File.sample(seed=2)
    task.inputs.output = File.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
