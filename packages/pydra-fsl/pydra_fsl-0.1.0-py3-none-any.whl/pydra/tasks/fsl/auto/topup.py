from fileformats.generic.file import File
from fileformats.medimage.nifti import Nifti1
from fileformats.text import TextFile
from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs
import typing as ty

input_fields = [
    (
        "in_file",
        Nifti1,
        {
            "help_string": "name of 4D file with images",
            "argstr": "--imain={in_file}",
            "mandatory": True,
        },
    ),
    (
        "encoding_file",
        TextFile,
        {
            "help_string": "name of text file with PE directions/times",
            "argstr": "--datain={encoding_file}",
            "mandatory": True,
            "xor": ["encoding_direction"],
        },
    ),
    (
        "encoding_direction",
        list,
        {
            "help_string": "encoding direction for automatic generation of encoding_file",
            "argstr": "--datain={encoding_direction}",
            "mandatory": True,
            "requires": ["readout_times"],
            "xor": ["encoding_file"],
        },
    ),
    (
        "readout_times",
        ty.List[File],
        {
            "help_string": "readout times (dwell times by # phase-encode steps minus 1)",
            "mandatory": True,
            "requires": ["encoding_direction"],
            "xor": ["encoding_file"],
        },
    ),
    (
        "out_base",
        Path,
        {
            "help_string": "base-name of output files (spline coefficients (Hz) and movement parameters)",
            "argstr": "--out={out_base}",
        },
    ),
    (
        "out_field",
        Path,
        {
            "help_string": "name of image file with field (Hz)",
            "argstr": "--fout={out_field}",
            "output_file_template": "{in_file}_field",
        },
    ),
    (
        "out_warp_prefix",
        str,
        "warpfield",
        {
            "help_string": "prefix for the warpfield images (in mm)",
            "argstr": "--dfout={out_warp_prefix}",
        },
    ),
    (
        "out_mat_prefix",
        str,
        "xfm",
        {
            "help_string": "prefix for the realignment matrices",
            "argstr": "--rbmout={out_mat_prefix}",
        },
    ),
    (
        "out_jac_prefix",
        str,
        "jac",
        {
            "help_string": "prefix for the warpfield images",
            "argstr": "--jacout={out_jac_prefix}",
        },
    ),
    (
        "out_corrected",
        Path,
        {
            "help_string": "name of 4D image file with unwarped images",
            "argstr": "--iout={out_corrected}",
            "output_file_template": "{in_file}_corrected",
        },
    ),
    (
        "out_logfile",
        Path,
        {
            "help_string": "name of log-file",
            "argstr": "--logout={out_logfile}",
            "output_file_template": "{in_file}_topup.log",
        },
    ),
    (
        "warp_res",
        ty.List[float],
        {
            "help_string": "(approximate) resolution (in mm) of warp basis for the different sub-sampling levels",
            "argstr": "--warpres={warp_res}",
        },
    ),
    (
        "subsamp",
        ty.List[int],
        {"help_string": "sub-sampling scheme", "argstr": "--subsamp={subsamp}"},
    ),
    (
        "fwhm",
        ty.List[float],
        {
            "help_string": "FWHM (in mm) of gaussian smoothing kernel",
            "argstr": "--fwhm={fwhm}",
        },
    ),
    (
        "config",
        ty.Any,
        "b02b0.cnf",
        {
            "help_string": "Name of config file specifying command line arguments",
            "argstr": "--config={config}",
        },
    ),
    (
        "max_iter",
        int,
        {
            "help_string": "max # of non-linear iterations",
            "argstr": "--miter={max_iter}",
        },
    ),
    (
        "reg_lambda",
        ty.List[float],
        {
            "help_string": "Weight of regularisation, default depending on --ssqlambda and --regmod switches.",
            "argstr": "--lambda={reg_lambda:0.}",
        },
    ),
    (
        "ssqlambda",
        ty.Any,
        {
            "help_string": "Weight lambda by the current value of the ssd. If used (=1), the effective weight of regularisation term becomes higher for the initial iterations, therefore initial steps are a little smoother than they would without weighting. This reduces the risk of finding a local minimum.",
            "argstr": "--ssqlambda={ssqlambda}",
        },
    ),
    (
        "regmod",
        str,
        {
            "help_string": "Regularisation term implementation. Defaults to bending_energy. Note that the two functions have vastly different scales. The membrane energy is based on the first derivatives and the bending energy on the second derivatives. The second derivatives will typically be much smaller than the first derivatives, so input lambda will have to be larger for bending_energy to yield approximately the same level of regularisation.",
            "argstr": "--regmod={regmod}",
        },
    ),
    (
        "estmov",
        ty.List[int],
        {"help_string": "estimate movements if set", "argstr": "--estmov={estmov}"},
    ),
    (
        "minmet",
        ty.List[int],
        {
            "help_string": "Minimisation method 0=Levenberg-Marquardt, 1=Scaled Conjugate Gradient",
            "argstr": "--minmet={minmet}",
        },
    ),
    (
        "splineorder",
        int,
        {
            "help_string": "order of spline, 2->Qadratic spline, 3->Cubic spline",
            "argstr": "--splineorder={splineorder}",
        },
    ),
    (
        "numprec",
        ty.Any,
        {
            "help_string": "Precision for representing Hessian, double or float.",
            "argstr": "--numprec={numprec}",
        },
    ),
    (
        "interp",
        str,
        {
            "help_string": "Image interpolation model, linear or spline.",
            "argstr": "--interp={interp}",
        },
    ),
    (
        "scale",
        bool,
        {
            "help_string": "If set (=1), the images are individually scaled to a common mean",
            "argstr": "--scale {int(scale)}",
        },
    ),
    (
        "regrid",
        ty.Any,
        {
            "help_string": "If set (=1), the calculations are done in a different grid",
            "argstr": "--regrid={regrid}",
        },
    ),
]
TOPUP_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("out_fieldcoef", File, {"help_string": "file containing the field coefficients"}),
    ("out_movpar", File, {"help_string": "movpar.txt output file"}),
    (
        "out_enc_file",
        File,
        {"help_string": "encoding directions file output for applytopup"},
    ),
    ("out_warps", ty.List[File], {"help_string": "warpfield images"}),
    ("out_jacs", ty.List[File], {"help_string": "Jacobian images"}),
    ("out_mats", ty.List[File], {"help_string": "realignment matrices"}),
]
TOPUP_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class TOPUP(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from fileformats.medimage.nifti import Nifti1
    >>> from fileformats.text import TextFile
    >>> from pydra.tasks.fsl.auto.topup import TOPUP

    >>> task = TOPUP()
    >>> task.inputs.in_file = Nifti1.mock("b0_b0rev.nii")
    >>> task.inputs.encoding_file = TextFile.mock("topup_encoding.txt")
    >>> task.cmdline
    'topup --config=b02b0.cnf --datain=topup_encoding.txt --imain=b0_b0rev.nii --out=b0_b0rev_base --iout=b0_b0rev_corrected.nii.gz --fout=b0_b0rev_field.nii.gz --jacout=jac --logout=b0_b0rev_topup.log --rbmout=xfm --dfout=warpfield'


    """

    input_spec = TOPUP_input_spec
    output_spec = TOPUP_output_spec
    executable = "topup"
