from fileformats.datascience.data import TextMatrix
from fileformats.generic.directory import Directory
from fileformats.generic.file import File
from fileformats.medimage.nifti import Nifti1
from fileformats.medimage.nifti import NiftiGz
from fileformats.medimage_fsl import Con
from pydra.engine import ShellCommandTask
from pydra.engine import specs
import typing as ty

input_fields = [
    (
        "cope_file",
        NiftiGz,
        {
            "help_string": "cope regressor data file",
            "argstr": "--copefile={cope_file}",
            "mandatory": True,
        },
    ),
    (
        "var_cope_file",
        NiftiGz,
        {
            "help_string": "varcope weightings data file",
            "argstr": "--varcopefile={var_cope_file}",
        },
    ),
    (
        "dof_var_cope_file",
        File,
        {
            "help_string": "dof data file for varcope data",
            "argstr": "--dofvarcopefile={dof_var_cope_file}",
        },
    ),
    (
        "mask_file",
        Nifti1,
        {
            "help_string": "mask file",
            "argstr": "--maskfile={mask_file}",
            "mandatory": True,
        },
    ),
    (
        "design_file",
        TextMatrix,
        {
            "help_string": "design matrix file",
            "argstr": "--designfile={design_file}",
            "mandatory": True,
        },
    ),
    (
        "t_con_file",
        Con,
        {
            "help_string": "ascii matrix specifying t-contrasts",
            "argstr": "--tcontrastsfile={t_con_file}",
            "mandatory": True,
        },
    ),
    (
        "f_con_file",
        File,
        {
            "help_string": "ascii matrix specifying f-contrasts",
            "argstr": "--fcontrastsfile={f_con_file}",
        },
    ),
    (
        "cov_split_file",
        TextMatrix,
        {
            "help_string": "ascii matrix specifying the groups the covariance is split into",
            "argstr": "--covsplitfile={cov_split_file}",
            "mandatory": True,
        },
    ),
    (
        "run_mode",
        ty.Any,
        {
            "help_string": "inference to perform",
            "argstr": "--runmode={run_mode}",
            "mandatory": True,
        },
    ),
    (
        "n_jumps",
        int,
        {"help_string": "number of jumps made by mcmc", "argstr": "--njumps={n_jumps}"},
    ),
    (
        "burnin",
        int,
        {
            "help_string": "number of jumps at start of mcmc to be discarded",
            "argstr": "--burnin={burnin}",
        },
    ),
    (
        "sample_every",
        int,
        {
            "help_string": "number of jumps for each sample",
            "argstr": "--sampleevery={sample_every}",
        },
    ),
    ("fix_mean", bool, {"help_string": "fix mean for tfit", "argstr": "--fixmean"}),
    (
        "infer_outliers",
        bool,
        {"help_string": "infer outliers - not for fe", "argstr": "--inferoutliers"},
    ),
    (
        "no_pe_outputs",
        bool,
        {"help_string": "do not output pe files", "argstr": "--nopeoutput"},
    ),
    (
        "sigma_dofs",
        int,
        {
            "help_string": "sigma (in mm) to use for Gaussian smoothing the DOFs in FLAME 2. Default is 1mm, -1 indicates no smoothing",
            "argstr": "--sigma_dofs={sigma_dofs}",
        },
    ),
    (
        "outlier_iter",
        int,
        {
            "help_string": "Number of max iterations to use when inferring outliers. Default is 12.",
            "argstr": "--ioni={outlier_iter}",
        },
    ),
    ("log_dir", Directory, "stats", {"help_string": "", "argstr": "--ld={log_dir}"}),
]
FLAMEO_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "pes",
        ty.List[File],
        {
            "help_string": "Parameter estimates for each column of the design matrix for each voxel"
        },
    ),
    (
        "res4d",
        ty.List[File],
        {"help_string": "Model fit residual mean-squared error for each time point"},
    ),
    ("copes", ty.List[File], {"help_string": "Contrast estimates for each contrast"}),
    (
        "var_copes",
        ty.List[File],
        {"help_string": "Variance estimates for each contrast"},
    ),
    ("zstats", ty.List[File], {"help_string": "z-stat file for each contrast"}),
    ("tstats", ty.List[File], {"help_string": "t-stat file for each contrast"}),
    ("zfstats", ty.List[File], {"help_string": "z stat file for each f contrast"}),
    ("fstats", ty.List[File], {"help_string": "f-stat file for each contrast"}),
    (
        "mrefvars",
        ty.List[File],
        {"help_string": "mean random effect variances for each contrast"},
    ),
    ("tdof", ty.List[File], {"help_string": "temporal dof file for each contrast"}),
    ("weights", ty.List[File], {"help_string": "weights file for each contrast"}),
    (
        "stats_dir",
        Directory,
        {"help_string": "directory storing model estimation output"},
    ),
]
FLAMEO_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class FLAMEO(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.datascience.data import TextMatrix
    >>> from fileformats.generic.directory import Directory
    >>> from fileformats.generic.file import File
    >>> from fileformats.medimage.nifti import Nifti1
    >>> from fileformats.medimage.nifti import NiftiGz
    >>> from fileformats.medimage_fsl import Con
    >>> from pydra.tasks.fsl.auto.flameo import FLAMEO

    >>> task = FLAMEO()
    >>> task.inputs.cope_file = NiftiGz.mock("cope.nii.gz")
    >>> task.inputs.var_cope_file = NiftiGz.mock("varcope.nii.gz")
    >>> task.inputs.dof_var_cope_file = File.mock()
    >>> task.inputs.mask_file = Nifti1.mock("mask.nii")
    >>> task.inputs.design_file = TextMatrix.mock("design.mat")
    >>> task.inputs.t_con_file = Con.mock("design.con")
    >>> task.inputs.f_con_file = File.mock()
    >>> task.inputs.cov_split_file = TextMatrix.mock("cov_split.mat")
    >>> task.inputs.run_mode = "fe"
    >>> task.inputs.log_dir = Directory.mock()
    >>> task.cmdline
    'flameo --copefile=cope.nii.gz --covsplitfile=cov_split.mat --designfile=design.mat --ld=stats --maskfile=mask.nii --runmode=fe --tcontrastsfile=design.con --varcopefile=varcope.nii.gz'


    """

    input_spec = FLAMEO_input_spec
    output_spec = FLAMEO_output_spec
    executable = "flameo"
