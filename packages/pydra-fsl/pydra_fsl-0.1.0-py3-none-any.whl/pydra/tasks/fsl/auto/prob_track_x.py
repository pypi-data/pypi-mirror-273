from fileformats.datascience.data import TextMatrix
from fileformats.generic.file import File
from fileformats.medimage.nifti import Nifti1
from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs
import typing as ty

input_fields = [
    (
        "mode",
        ty.Any,
        {
            "help_string": "options: simple (single seed voxel), seedmask (mask of seed voxels), twomask_symm (two bet binary masks)",
            "argstr": "--mode={mode}",
        },
    ),
    (
        "mask2",
        File,
        {
            "help_string": "second bet binary mask (in diffusion space) in twomask_symm mode",
            "argstr": "--mask2={mask2}",
        },
    ),
    (
        "mesh",
        File,
        {
            "help_string": "Freesurfer-type surface descriptor (in ascii format)",
            "argstr": "--mesh={mesh}",
        },
    ),
    ("thsamples", ty.List[Nifti1], {"help_string": "", "mandatory": True}),
    ("phsamples", ty.List[Nifti1], {"help_string": "", "mandatory": True}),
    ("fsamples", ty.List[Nifti1], {"help_string": "", "mandatory": True}),
    (
        "samples_base_name",
        str,
        "merged",
        {
            "help_string": "the rootname/base_name for samples files",
            "argstr": "--samples={samples_base_name}",
        },
    ),
    (
        "mask",
        Nifti1,
        {
            "help_string": "bet binary mask file in diffusion space",
            "argstr": "-m {mask}",
            "mandatory": True,
        },
    ),
    (
        "seed",
        ty.Any,
        {
            "help_string": "seed volume(s), or voxel(s) or freesurfer label file",
            "argstr": "--seed={seed}",
            "mandatory": True,
        },
    ),
    (
        "target_masks",
        ty.List[Nifti1],
        {
            "help_string": "list of target masks - required for seeds_to_targets classification",
            "argstr": "--targetmasks={target_masks}",
        },
    ),
    (
        "waypoints",
        File,
        {
            "help_string": "waypoint mask or ascii list of waypoint masks - only keep paths going through ALL the masks",
            "argstr": "--waypoints={waypoints}",
        },
    ),
    (
        "network",
        bool,
        {
            "help_string": "activate network mode - only keep paths going through at least one seed mask (required if multiple seed masks)",
            "argstr": "--network",
        },
    ),
    (
        "seed_ref",
        File,
        {
            "help_string": "reference vol to define seed space in simple mode - diffusion space assumed if absent",
            "argstr": "--seedref={seed_ref}",
        },
    ),
    (
        "out_dir",
        Path,
        {
            "help_string": "directory to put the final volumes in",
            "argstr": "--dir={out_dir}",
        },
    ),
    (
        "force_dir",
        bool,
        True,
        {
            "help_string": "use the actual directory name given - i.e. do not add + to make a new directory",
            "argstr": "--forcedir",
        },
    ),
    (
        "opd",
        bool,
        True,
        {"help_string": "outputs path distributions", "argstr": "--opd"},
    ),
    (
        "correct_path_distribution",
        bool,
        {
            "help_string": "correct path distribution for the length of the pathways",
            "argstr": "--pd",
        },
    ),
    ("os2t", bool, {"help_string": "Outputs seeds to targets", "argstr": "--os2t"}),
    (
        "avoid_mp",
        File,
        {
            "help_string": "reject pathways passing through locations given by this mask",
            "argstr": "--avoid={avoid_mp}",
        },
    ),
    (
        "stop_mask",
        File,
        {
            "help_string": "stop tracking at locations given by this mask file",
            "argstr": "--stop={stop_mask}",
        },
    ),
    (
        "xfm",
        TextMatrix,
        {
            "help_string": "transformation matrix taking seed space to DTI space (either FLIRT matrix or FNIRT warp_field) - default is identity",
            "argstr": "--xfm={xfm}",
        },
    ),
    (
        "inv_xfm",
        File,
        {
            "help_string": "transformation matrix taking DTI space to seed space (compulsory when using a warp_field for seeds_to_dti)",
            "argstr": "--invxfm={inv_xfm}",
        },
    ),
    (
        "n_samples",
        int,
        5000,
        {
            "help_string": "number of samples - default=5000",
            "argstr": "--nsamples={n_samples}",
        },
    ),
    (
        "n_steps",
        int,
        {
            "help_string": "number of steps per sample - default=2000",
            "argstr": "--nsteps={n_steps}",
        },
    ),
    (
        "dist_thresh",
        float,
        {
            "help_string": "discards samples shorter than this threshold (in mm - default=0)",
            "argstr": "--distthresh={dist_thresh:.3}",
        },
    ),
    (
        "c_thresh",
        float,
        {
            "help_string": "curvature threshold - default=0.2",
            "argstr": "--cthr={c_thresh:.3}",
        },
    ),
    (
        "sample_random_points",
        bool,
        {
            "help_string": "sample random points within seed voxels",
            "argstr": "--sampvox",
        },
    ),
    (
        "step_length",
        float,
        {
            "help_string": "step_length in mm - default=0.5",
            "argstr": "--steplength={step_length:.3}",
        },
    ),
    (
        "loop_check",
        bool,
        {
            "help_string": "perform loop_checks on paths - slower, but allows lower curvature threshold",
            "argstr": "--loopcheck",
        },
    ),
    (
        "use_anisotropy",
        bool,
        {"help_string": "use anisotropy to constrain tracking", "argstr": "--usef"},
    ),
    (
        "rand_fib",
        ty.Any,
        {
            "help_string": "options: 0 - default, 1 - to randomly sample initial fibres (with f > fibthresh), 2 - to sample in proportion fibres (with f>fibthresh) to f, 3 - to sample ALL populations at random (even if f<fibthresh)",
            "argstr": "--randfib={rand_fib}",
        },
    ),
    (
        "fibst",
        int,
        {
            "help_string": "force a starting fibre for tracking - default=1, i.e. first fibre orientation. Only works if randfib==0",
            "argstr": "--fibst={fibst}",
        },
    ),
    (
        "mod_euler",
        bool,
        {"help_string": "use modified euler streamlining", "argstr": "--modeuler"},
    ),
    ("random_seed", bool, {"help_string": "random seed", "argstr": "--rseed"}),
    (
        "s2tastext",
        bool,
        {
            "help_string": "output seed-to-target counts as a text file (useful when seeding from a mesh)",
            "argstr": "--s2tastext",
        },
    ),
    (
        "verbose",
        ty.Any,
        {
            "help_string": "Verbose level, [0-2]. Level 2 is required to output particle files.",
            "argstr": "--verbose={verbose}",
        },
    ),
]
ProbTrackX_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "log",
        File,
        {"help_string": "path/name of a text record of the command that was run"},
    ),
    (
        "fdt_paths",
        ty.List[File],
        {
            "help_string": "path/name of a 3D image file containing the output connectivity distribution to the seed mask"
        },
    ),
    (
        "way_total",
        File,
        {
            "help_string": "path/name of a text file containing a single number corresponding to the total number of generated tracts that have not been rejected by inclusion/exclusion mask criteria"
        },
    ),
    (
        "targets",
        ty.List[File],
        {"help_string": "a list with all generated seeds_to_target files"},
    ),
    (
        "particle_files",
        ty.List[File],
        {
            "help_string": "Files describing all of the tract samples. Generated only if verbose is set to 2"
        },
    ),
]
ProbTrackX_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ProbTrackX(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.datascience.data import TextMatrix
    >>> from fileformats.generic.file import File
    >>> from fileformats.medimage.nifti import Nifti1
    >>> from pydra.tasks.fsl.auto.prob_track_x import ProbTrackX

    >>> task = ProbTrackX()
    >>> task.inputs.mode = "seedmask"
    >>> task.inputs.mask2 = File.mock()
    >>> task.inputs.mesh = File.mock()
    >>> task.inputs.thsamples = [Nifti1.mock("m"), Nifti1.mock("e"), Nifti1.mock("r"), Nifti1.mock("g"), Nifti1.mock("e"), Nifti1.mock("d"), Nifti1.mock("_"), Nifti1.mock("t"), Nifti1.mock("h"), Nifti1.mock("s"), Nifti1.mock("a"), Nifti1.mock("m"), Nifti1.mock("p"), Nifti1.mock("l"), Nifti1.mock("e"), Nifti1.mock("s"), Nifti1.mock("."), Nifti1.mock("n"), Nifti1.mock("i"), Nifti1.mock("i")]
    >>> task.inputs.phsamples = [Nifti1.mock("m"), Nifti1.mock("e"), Nifti1.mock("r"), Nifti1.mock("g"), Nifti1.mock("e"), Nifti1.mock("d"), Nifti1.mock("_"), Nifti1.mock("p"), Nifti1.mock("h"), Nifti1.mock("s"), Nifti1.mock("a"), Nifti1.mock("m"), Nifti1.mock("p"), Nifti1.mock("l"), Nifti1.mock("e"), Nifti1.mock("s"), Nifti1.mock("."), Nifti1.mock("n"), Nifti1.mock("i"), Nifti1.mock("i")]
    >>> task.inputs.fsamples = [Nifti1.mock("m"), Nifti1.mock("e"), Nifti1.mock("r"), Nifti1.mock("g"), Nifti1.mock("e"), Nifti1.mock("d"), Nifti1.mock("_"), Nifti1.mock("f"), Nifti1.mock("s"), Nifti1.mock("a"), Nifti1.mock("m"), Nifti1.mock("p"), Nifti1.mock("l"), Nifti1.mock("e"), Nifti1.mock("s"), Nifti1.mock("."), Nifti1.mock("n"), Nifti1.mock("i"), Nifti1.mock("i")]
    >>> task.inputs.samples_base_name = "merged"
    >>> task.inputs.mask = Nifti1.mock("mask.nii")
    >>> task.inputs.seed = "MASK_average_thal_right.nii"
    >>> task.inputs.target_masks = [Nifti1.mock("targets_MASK1.nii"), Nifti1.mock("targets_MASK2.nii")]
    >>> task.inputs.waypoints = File.mock()
    >>> task.inputs.seed_ref = File.mock()
    >>> task.inputs.out_dir = "."
    >>> task.inputs.force_dir = True
    >>> task.inputs.opd = True
    >>> task.inputs.os2t = True
    >>> task.inputs.avoid_mp = File.mock()
    >>> task.inputs.stop_mask = File.mock()
    >>> task.inputs.xfm = TextMatrix.mock("trans.mat")
    >>> task.inputs.inv_xfm = File.mock()
    >>> task.inputs.n_samples = 3
    >>> task.inputs.n_steps = 10
    >>> task.cmdline
    'probtrackx --forcedir -m mask.nii --mode=seedmask --nsamples=3 --nsteps=10 --opd --os2t --dir=. --samples=merged --seed=MASK_average_thal_right.nii --targetmasks=targets.txt --xfm=trans.mat'


    """

    input_spec = ProbTrackX_input_spec
    output_spec = ProbTrackX_output_spec
    executable = "probtrackx"
