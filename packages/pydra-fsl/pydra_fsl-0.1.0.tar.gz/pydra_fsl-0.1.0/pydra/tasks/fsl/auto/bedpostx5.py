from fileformats.generic.directory import Directory
from fileformats.generic.file import File
from fileformats.medimage.diffusion import Bval
from fileformats.medimage.diffusion import Bvec
from fileformats.medimage.nifti import Nifti1
from pydra.engine import ShellCommandTask
from pydra.engine import specs
import typing as ty

input_fields = [
    (
        "dwi",
        Nifti1,
        {"help_string": "diffusion weighted image data file", "mandatory": True},
    ),
    ("mask", Nifti1, {"help_string": "bet binary mask file", "mandatory": True}),
    ("bvecs", Bvec, {"help_string": "b vectors file", "mandatory": True}),
    ("bvals", Bval, {"help_string": "b values file", "mandatory": True}),
    ("logdir", Directory, {"help_string": "", "argstr": "--logdir={logdir}"}),
    (
        "n_fibres",
        ty.Any,
        {
            "help_string": "Maximum number of fibres to fit in each voxel",
            "argstr": "-n {n_fibres}",
            "mandatory": True,
        },
    ),
    (
        "model",
        ty.Any,
        {
            "help_string": "use monoexponential (1, default, required for single-shell) or multiexponential (2, multi-shell) model",
            "argstr": "-model {model}",
        },
    ),
    ("fudge", int, {"help_string": "ARD fudge factor", "argstr": "-w {fudge}"}),
    (
        "n_jumps",
        int,
        5000,
        {"help_string": "Num of jumps to be made by MCMC", "argstr": "-j {n_jumps}"},
    ),
    (
        "burn_in",
        ty.Any,
        0,
        {
            "help_string": "Total num of jumps at start of MCMC to be discarded",
            "argstr": "-b {burn_in}",
        },
    ),
    (
        "sample_every",
        ty.Any,
        1,
        {
            "help_string": "Num of jumps for each sample (MCMC)",
            "argstr": "-s {sample_every}",
        },
    ),
    (
        "out_dir",
        Directory,
        {
            "help_string": "output directory",
            "argstr": "{out_dir}",
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "gradnonlin",
        bool,
        {
            "help_string": "consider gradient nonlinearities, default off",
            "argstr": "-g",
        },
    ),
    ("grad_dev", File, {"help_string": "grad_dev file, if gradnonlin, -g is True"}),
    ("use_gpu", bool, {"help_string": "Use the GPU version of bedpostx"}),
    (
        "burn_in_no_ard",
        ty.Any,
        0,
        {
            "help_string": "num of burnin jumps before the ard is imposed",
            "argstr": "--burnin_noard={burn_in_no_ard}",
        },
    ),
    (
        "update_proposal_every",
        ty.Any,
        40,
        {
            "help_string": "Num of jumps for each update to the proposal density std (MCMC)",
            "argstr": "--updateproposalevery={update_proposal_every}",
        },
    ),
    (
        "seed",
        int,
        {
            "help_string": "seed for pseudo random number generator",
            "argstr": "--seed={seed}",
        },
    ),
    (
        "no_ard",
        bool,
        {
            "help_string": "Turn ARD off on all fibres",
            "argstr": "--noard",
            "xor": ("no_ard", "all_ard"),
        },
    ),
    (
        "all_ard",
        bool,
        {
            "help_string": "Turn ARD on on all fibres",
            "argstr": "--allard",
            "xor": ("no_ard", "all_ard"),
        },
    ),
    (
        "no_spat",
        bool,
        {
            "help_string": "Initialise with tensor, not spatially",
            "argstr": "--nospat",
            "xor": ("no_spat", "non_linear", "cnlinear"),
        },
    ),
    (
        "non_linear",
        bool,
        {
            "help_string": "Initialise with nonlinear fitting",
            "argstr": "--nonlinear",
            "xor": ("no_spat", "non_linear", "cnlinear"),
        },
    ),
    (
        "cnlinear",
        bool,
        {
            "help_string": "Initialise with constrained nonlinear fitting",
            "argstr": "--cnonlinear",
            "xor": ("no_spat", "non_linear", "cnlinear"),
        },
    ),
    (
        "rician",
        bool,
        {"help_string": "use Rician noise modeling", "argstr": "--rician"},
    ),
    (
        "f0_noard",
        bool,
        {
            "help_string": "Noise floor model: add to the model an unattenuated signal compartment f0",
            "argstr": "--f0",
            "xor": ["f0_noard", "f0_ard"],
        },
    ),
    (
        "f0_ard",
        bool,
        {
            "help_string": "Noise floor model: add to the model an unattenuated signal compartment f0",
            "argstr": "--f0 --ardf0",
            "xor": ["f0_noard", "f0_ard", "all_ard"],
        },
    ),
    (
        "force_dir",
        bool,
        True,
        {
            "help_string": "use the actual directory name given (do not add + to make a new directory)",
            "argstr": "--forcedir",
        },
    ),
]
BEDPOSTX5_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("mean_dsamples", File, {"help_string": "Mean of distribution on diffusivity d"}),
    (
        "mean_fsamples",
        ty.List[File],
        {"help_string": "Mean of distribution on f anisotropy"},
    ),
    (
        "mean_S0samples",
        File,
        {"help_string": "Mean of distribution on T2wbaseline signal intensity S0"},
    ),
    ("mean_phsamples", ty.List[File], {"help_string": "Mean of distribution on phi"}),
    ("mean_thsamples", ty.List[File], {"help_string": "Mean of distribution on theta"}),
    (
        "merged_thsamples",
        ty.List[File],
        {"help_string": "Samples from the distribution on theta"},
    ),
    (
        "merged_phsamples",
        ty.List[File],
        {"help_string": "Samples from the distribution on phi"},
    ),
    (
        "merged_fsamples",
        ty.List[File],
        {"help_string": "Samples from the distribution on anisotropic volume fraction"},
    ),
    (
        "dyads",
        ty.List[File],
        {"help_string": "Mean of PDD distribution in vector form."},
    ),
    ("dyads_dispersion", ty.List[File], {"help_string": "Dispersion"}),
]
BEDPOSTX5_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class BEDPOSTX5(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.directory import Directory
    >>> from fileformats.generic.file import File
    >>> from fileformats.medimage.diffusion import Bval
    >>> from fileformats.medimage.diffusion import Bvec
    >>> from fileformats.medimage.nifti import Nifti1
    >>> from pydra.tasks.fsl.auto.bedpostx5 import BEDPOSTX5

    >>> task = BEDPOSTX5()
    >>> task.inputs.dwi = Nifti1.mock("diffusion.nii")
    >>> task.inputs.mask = Nifti1.mock("mask.nii")
    >>> task.inputs.bvecs = Bvec.mock("bvecs")
    >>> task.inputs.bvals = Bval.mock("bvals")
    >>> task.inputs.logdir = Directory.mock()
    >>> task.inputs.n_fibres = 1
    >>> task.inputs.out_dir = Directory.mock()
    >>> task.inputs.grad_dev = File.mock()
    >>> task.cmdline
    'bedpostx bedpostx -b 0 --burnin_noard=0 --forcedir -n 1 -j 5000 -s 1 --updateproposalevery=40'


    """

    input_spec = BEDPOSTX5_input_spec
    output_spec = BEDPOSTX5_output_spec
    executable = "bedpostx"
