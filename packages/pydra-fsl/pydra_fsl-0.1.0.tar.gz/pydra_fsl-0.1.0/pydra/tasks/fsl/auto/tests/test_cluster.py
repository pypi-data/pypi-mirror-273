from fileformats.generic.file import File
from fileformats.medimage.nifti import NiftiGz
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.cluster import Cluster
import pytest


@pytest.mark.xfail
def test_cluster_1():
    task = Cluster()
    task.inputs.in_file = NiftiGz.sample(seed=0)
    task.inputs.cope_file = File.sample(seed=12)
    task.inputs.fractional = False
    task.inputs.use_mm = False
    task.inputs.find_min = False
    task.inputs.no_table = False
    task.inputs.minclustersize = False
    task.inputs.xfm_file = File.sample(seed=21)
    task.inputs.std_space_file = File.sample(seed=22)
    task.inputs.warpfield_file = File.sample(seed=24)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_cluster_2():
    task = Cluster()
    task.inputs.in_file = NiftiGz.sample(seed=0)
    task.inputs.threshold = 2.3
    task.inputs.out_localmax_txt_file = "stats.txt"
    task.inputs.use_mm = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
