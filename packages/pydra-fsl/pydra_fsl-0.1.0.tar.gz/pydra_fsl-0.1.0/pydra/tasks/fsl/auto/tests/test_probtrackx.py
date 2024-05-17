from fileformats.datascience.data import TextMatrix
from fileformats.generic.file import File
from fileformats.medimage.nifti import Nifti1
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.prob_track_x import ProbTrackX
import pytest


@pytest.mark.xfail
def test_probtrackx_1():
    task = ProbTrackX()
    task.inputs.mask2 = File.sample(seed=1)
    task.inputs.mesh = File.sample(seed=2)
    task.inputs.thsamples = [Nifti1.sample(seed=3)]
    task.inputs.phsamples = [Nifti1.sample(seed=4)]
    task.inputs.fsamples = [Nifti1.sample(seed=5)]
    task.inputs.samples_base_name = "merged"
    task.inputs.mask = Nifti1.sample(seed=7)
    task.inputs.target_masks = [Nifti1.sample(seed=9)]
    task.inputs.waypoints = File.sample(seed=10)
    task.inputs.seed_ref = File.sample(seed=12)
    task.inputs.force_dir = True
    task.inputs.opd = True
    task.inputs.avoid_mp = File.sample(seed=18)
    task.inputs.stop_mask = File.sample(seed=19)
    task.inputs.xfm = TextMatrix.sample(seed=20)
    task.inputs.inv_xfm = File.sample(seed=21)
    task.inputs.n_samples = 5000
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_probtrackx_2():
    task = ProbTrackX()
    task.inputs.mode = "seedmask"
    task.inputs.thsamples = [Nifti1.sample(seed=3)]
    task.inputs.phsamples = [Nifti1.sample(seed=4)]
    task.inputs.fsamples = [Nifti1.sample(seed=5)]
    task.inputs.samples_base_name = "merged"
    task.inputs.mask = Nifti1.sample(seed=7)
    task.inputs.seed = "MASK_average_thal_right.nii"
    task.inputs.target_masks = [Nifti1.sample(seed=9)]
    task.inputs.out_dir = "."
    task.inputs.force_dir = True
    task.inputs.opd = True
    task.inputs.os2t = True
    task.inputs.xfm = TextMatrix.sample(seed=20)
    task.inputs.n_samples = 3
    task.inputs.n_steps = 10
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
