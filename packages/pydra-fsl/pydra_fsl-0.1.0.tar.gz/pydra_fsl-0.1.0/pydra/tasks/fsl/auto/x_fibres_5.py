from fileformats.generic.directory import Directory
from fileformats.generic.file import File
from pydra.engine import ShellCommandTask
from pydra.engine import specs
import typing as ty

input_fields = [
    (
        "gradnonlin",
        File,
        {
            "help_string": "gradient file corresponding to slice",
            "argstr": "--gradnonlin={gradnonlin}",
        },
    ),
    (
        "dwi",
        File,
        {
            "help_string": "diffusion weighted image data file",
            "argstr": "--data={dwi}",
            "mandatory": True,
        },
    ),
    (
        "mask",
        File,
        {
            "help_string": "brain binary mask file (i.e. from BET)",
            "argstr": "--mask={mask}",
            "mandatory": True,
        },
    ),
    (
        "bvecs",
        File,
        {
            "help_string": "b vectors file",
            "argstr": "--bvecs={bvecs}",
            "mandatory": True,
        },
    ),
    (
        "bvals",
        File,
        {
            "help_string": "b values file",
            "argstr": "--bvals={bvals}",
            "mandatory": True,
        },
    ),
    ("logdir", Directory, ".", {"help_string": "", "argstr": "--logdir={logdir}"}),
    (
        "n_fibres",
        ty.Any,
        {
            "help_string": "Maximum number of fibres to fit in each voxel",
            "argstr": "--nfibres={n_fibres}",
            "mandatory": True,
        },
    ),
    (
        "model",
        ty.Any,
        {
            "help_string": "use monoexponential (1, default, required for single-shell) or multiexponential (2, multi-shell) model",
            "argstr": "--model={model}",
        },
    ),
    ("fudge", int, {"help_string": "ARD fudge factor", "argstr": "--fudge={fudge}"}),
    (
        "n_jumps",
        int,
        5000,
        {
            "help_string": "Num of jumps to be made by MCMC",
            "argstr": "--njumps={n_jumps}",
        },
    ),
    (
        "burn_in",
        ty.Any,
        0,
        {
            "help_string": "Total num of jumps at start of MCMC to be discarded",
            "argstr": "--burnin={burn_in}",
        },
    ),
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
        "sample_every",
        ty.Any,
        1,
        {
            "help_string": "Num of jumps for each sample (MCMC)",
            "argstr": "--sampleevery={sample_every}",
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
XFibres5_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "dyads",
        ty.List[File],
        {"help_string": "Mean of PDD distribution in vector form."},
    ),
    (
        "fsamples",
        ty.List[File],
        {"help_string": "Samples from the distribution on f anisotropy"},
    ),
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
    (
        "mean_tausamples",
        File,
        {"help_string": "Mean of distribution on tau samples (only with rician noise)"},
    ),
    ("phsamples", ty.List[File], {"help_string": "phi samples, per fiber"}),
    ("thsamples", ty.List[File], {"help_string": "theta samples, per fiber"}),
]
XFibres5_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class XFibres5(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.directory import Directory
    >>> from fileformats.generic.file import File
    >>> from pydra.tasks.fsl.auto.x_fibres_5 import XFibres5

    """

    input_spec = XFibres5_input_spec
    output_spec = XFibres5_output_spec
    executable = "xfibres"
