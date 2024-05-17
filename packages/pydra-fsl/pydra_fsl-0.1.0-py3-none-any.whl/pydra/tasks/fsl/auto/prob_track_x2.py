from fileformats.generic.file import File
from fileformats.medimage.nifti import NiftiGz
from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs
import typing as ty

input_fields = [
    (
        "simple",
        bool,
        {
            "help_string": "rack from a list of voxels (seed must be a ASCII list of coordinates)",
            "argstr": "--simple",
        },
    ),
    (
        "fopd",
        File,
        {
            "help_string": "Other mask for binning tract distribution",
            "argstr": "--fopd={fopd}",
        },
    ),
    (
        "waycond",
        ty.Any,
        {
            "help_string": 'Waypoint condition. Either "AND" (default) or "OR"',
            "argstr": "--waycond={waycond}",
        },
    ),
    (
        "wayorder",
        bool,
        {
            "help_string": "Reject streamlines that do not hit waypoints in given order. Only valid if waycond=AND",
            "argstr": "--wayorder",
        },
    ),
    (
        "onewaycondition",
        bool,
        {
            "help_string": "Apply waypoint conditions to each half tract separately",
            "argstr": "--onewaycondition",
        },
    ),
    (
        "omatrix1",
        bool,
        {
            "help_string": "Output matrix1 - SeedToSeed Connectivity",
            "argstr": "--omatrix1",
        },
    ),
    (
        "distthresh1",
        float,
        {
            "help_string": "Discards samples (in matrix1) shorter than this threshold (in mm - default=0)",
            "argstr": "--distthresh1={distthresh1:.3}",
        },
    ),
    (
        "omatrix2",
        bool,
        {
            "help_string": "Output matrix2 - SeedToLowResMask",
            "argstr": "--omatrix2",
            "requires": ["target2"],
        },
    ),
    (
        "target2",
        File,
        {
            "help_string": "Low resolution binary brain mask for storing connectivity distribution in matrix2 mode",
            "argstr": "--target2={target2}",
        },
    ),
    (
        "omatrix3",
        bool,
        {
            "help_string": "Output matrix3 (NxN connectivity matrix)",
            "argstr": "--omatrix3",
            "requires": ["target3", "lrtarget3"],
        },
    ),
    (
        "target3",
        File,
        {
            "help_string": "Mask used for NxN connectivity matrix (or Nxn if lrtarget3 is set)",
            "argstr": "--target3={target3}",
        },
    ),
    (
        "lrtarget3",
        File,
        {
            "help_string": "Column-space mask used for Nxn connectivity matrix",
            "argstr": "--lrtarget3={lrtarget3}",
        },
    ),
    (
        "distthresh3",
        float,
        {
            "help_string": "Discards samples (in matrix3) shorter than this threshold (in mm - default=0)",
            "argstr": "--distthresh3={distthresh3:.3}",
        },
    ),
    (
        "omatrix4",
        bool,
        {
            "help_string": "Output matrix4 - DtiMaskToSeed (special Oxford Sparse Format)",
            "argstr": "--omatrix4",
        },
    ),
    (
        "colmask4",
        File,
        {
            "help_string": "Mask for columns of matrix4 (default=seed mask)",
            "argstr": "--colmask4={colmask4}",
        },
    ),
    (
        "target4",
        File,
        {"help_string": "Brain mask in DTI space", "argstr": "--target4={target4}"},
    ),
    (
        "meshspace",
        ty.Any,
        {
            "help_string": 'Mesh reference space - either "caret" (default) or "freesurfer" or "first" or "vox"',
            "argstr": "--meshspace={meshspace}",
        },
    ),
    ("thsamples", ty.List[NiftiGz], {"help_string": "", "mandatory": True}),
    ("phsamples", ty.List[NiftiGz], {"help_string": "", "mandatory": True}),
    ("fsamples", ty.List[NiftiGz], {"help_string": "", "mandatory": True}),
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
        NiftiGz,
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
        ty.List[File],
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
        File,
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
ProbTrackX2_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "network_matrix",
        File,
        {"help_string": "the network matrix generated by --omatrix1 option"},
    ),
    (
        "matrix1_dot",
        File,
        {"help_string": "Output matrix1.dot - SeedToSeed Connectivity"},
    ),
    (
        "lookup_tractspace",
        File,
        {"help_string": "lookup_tractspace generated by --omatrix2 option"},
    ),
    ("matrix2_dot", File, {"help_string": "Output matrix2.dot - SeedToLowResMask"}),
    ("matrix3_dot", File, {"help_string": "Output matrix3 - NxN connectivity matrix"}),
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
ProbTrackX2_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ProbTrackX2(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from fileformats.medimage.nifti import NiftiGz
    >>> from pydra.tasks.fsl.auto.prob_track_x2 import ProbTrackX2

    >>> task = ProbTrackX2()
    >>> task.inputs.fopd = File.mock()
    >>> task.inputs.target2 = File.mock()
    >>> task.inputs.target3 = File.mock()
    >>> task.inputs.lrtarget3 = File.mock()
    >>> task.inputs.colmask4 = File.mock()
    >>> task.inputs.target4 = File.mock()
    >>> task.inputs.thsamples = [NiftiGz.mock("m"), NiftiGz.mock("e"), NiftiGz.mock("r"), NiftiGz.mock("g"), NiftiGz.mock("e"), NiftiGz.mock("d"), NiftiGz.mock("_"), NiftiGz.mock("t"), NiftiGz.mock("h"), NiftiGz.mock("1"), NiftiGz.mock("s"), NiftiGz.mock("a"), NiftiGz.mock("m"), NiftiGz.mock("p"), NiftiGz.mock("l"), NiftiGz.mock("e"), NiftiGz.mock("s"), NiftiGz.mock("."), NiftiGz.mock("n"), NiftiGz.mock("i"), NiftiGz.mock("i"), NiftiGz.mock("."), NiftiGz.mock("g"), NiftiGz.mock("z")]
    >>> task.inputs.phsamples = [NiftiGz.mock("m"), NiftiGz.mock("e"), NiftiGz.mock("r"), NiftiGz.mock("g"), NiftiGz.mock("e"), NiftiGz.mock("d"), NiftiGz.mock("_"), NiftiGz.mock("p"), NiftiGz.mock("h"), NiftiGz.mock("1"), NiftiGz.mock("s"), NiftiGz.mock("a"), NiftiGz.mock("m"), NiftiGz.mock("p"), NiftiGz.mock("l"), NiftiGz.mock("e"), NiftiGz.mock("s"), NiftiGz.mock("."), NiftiGz.mock("n"), NiftiGz.mock("i"), NiftiGz.mock("i"), NiftiGz.mock("."), NiftiGz.mock("g"), NiftiGz.mock("z")]
    >>> task.inputs.fsamples = [NiftiGz.mock("m"), NiftiGz.mock("e"), NiftiGz.mock("r"), NiftiGz.mock("g"), NiftiGz.mock("e"), NiftiGz.mock("d"), NiftiGz.mock("_"), NiftiGz.mock("f"), NiftiGz.mock("1"), NiftiGz.mock("s"), NiftiGz.mock("a"), NiftiGz.mock("m"), NiftiGz.mock("p"), NiftiGz.mock("l"), NiftiGz.mock("e"), NiftiGz.mock("s"), NiftiGz.mock("."), NiftiGz.mock("n"), NiftiGz.mock("i"), NiftiGz.mock("i"), NiftiGz.mock("."), NiftiGz.mock("g"), NiftiGz.mock("z")]
    >>> task.inputs.mask = NiftiGz.mock("nodif_brain_mask.nii.gz")
    >>> task.inputs.seed = "seed_source.nii.gz"
    >>> task.inputs.waypoints = File.mock()
    >>> task.inputs.seed_ref = File.mock()
    >>> task.inputs.out_dir = "."
    >>> task.inputs.avoid_mp = File.mock()
    >>> task.inputs.stop_mask = File.mock()
    >>> task.inputs.xfm = File.mock()
    >>> task.inputs.inv_xfm = File.mock()
    >>> task.inputs.n_samples = 3
    >>> task.inputs.n_steps = 10
    >>> task.cmdline
    'probtrackx2 --forcedir -m nodif_brain_mask.nii.gz --nsamples=3 --nsteps=10 --opd --dir=. --samples=merged --seed=seed_source.nii.gz'


    """

    input_spec = ProbTrackX2_input_spec
    output_spec = ProbTrackX2_output_spec
    executable = "probtrackx2"
