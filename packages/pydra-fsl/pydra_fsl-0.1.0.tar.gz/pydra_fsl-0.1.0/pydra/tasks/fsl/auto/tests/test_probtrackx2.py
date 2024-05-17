from fileformats.generic.file import File
from fileformats.medimage.nifti import NiftiGz
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.prob_track_x2 import ProbTrackX2
import pytest


@pytest.mark.xfail
def test_probtrackx2_1():
    task = ProbTrackX2()
    task.inputs.fopd = File.sample(seed=1)
    task.inputs.target2 = File.sample(seed=8)
    task.inputs.target3 = File.sample(seed=10)
    task.inputs.lrtarget3 = File.sample(seed=11)
    task.inputs.colmask4 = File.sample(seed=14)
    task.inputs.target4 = File.sample(seed=15)
    task.inputs.thsamples = [NiftiGz.sample(seed=17)]
    task.inputs.phsamples = [NiftiGz.sample(seed=18)]
    task.inputs.fsamples = [NiftiGz.sample(seed=19)]
    task.inputs.samples_base_name = "merged"
    task.inputs.mask = NiftiGz.sample(seed=21)
    task.inputs.target_masks = [File.sample(seed=23)]
    task.inputs.waypoints = File.sample(seed=24)
    task.inputs.seed_ref = File.sample(seed=26)
    task.inputs.force_dir = True
    task.inputs.opd = True
    task.inputs.avoid_mp = File.sample(seed=32)
    task.inputs.stop_mask = File.sample(seed=33)
    task.inputs.xfm = File.sample(seed=34)
    task.inputs.inv_xfm = File.sample(seed=35)
    task.inputs.n_samples = 5000
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_probtrackx2_2():
    task = ProbTrackX2()
    task.inputs.thsamples = [NiftiGz.sample(seed=17)]
    task.inputs.phsamples = [NiftiGz.sample(seed=18)]
    task.inputs.fsamples = [NiftiGz.sample(seed=19)]
    task.inputs.mask = NiftiGz.sample(seed=21)
    task.inputs.seed = "seed_source.nii.gz"
    task.inputs.out_dir = "."
    task.inputs.n_samples = 3
    task.inputs.n_steps = 10
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
