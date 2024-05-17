from fileformats.medimage.nifti import Nifti1
from fileformats.medimage.nifti import NiftiGz
from fileformats.text import TextFile
from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs
import typing as ty

input_fields = [
    (
        "in_files",
        ty.List[Nifti1],
        {
            "help_string": "name of file with images",
            "argstr": "--imain={in_files}",
            "mandatory": True,
            "sep": ",",
        },
    ),
    (
        "encoding_file",
        TextFile,
        {
            "help_string": "name of text file with PE directions/times",
            "argstr": "--datain={encoding_file}",
            "mandatory": True,
        },
    ),
    (
        "in_index",
        list,
        {
            "help_string": "comma separated list of indices corresponding to --datain",
            "argstr": "--inindex={in_index}",
            "sep": ",",
        },
    ),
    (
        "in_topup_fieldcoef",
        NiftiGz,
        {
            "help_string": "topup file containing the field coefficients",
            "argstr": "--topup={in_topup_fieldcoef}",
            "copyfile": False,
            "requires": ["in_topup_movpar"],
        },
    ),
    (
        "in_topup_movpar",
        TextFile,
        {
            "help_string": "topup movpar.txt file",
            "copyfile": False,
            "requires": ["in_topup_fieldcoef"],
        },
    ),
    (
        "out_corrected",
        Path,
        {
            "help_string": "output (warped) image",
            "argstr": "--out={out_corrected}",
            "output_file_template": "{in_files}_corrected",
        },
    ),
    (
        "method",
        ty.Any,
        {
            "help_string": "use jacobian modulation (jac) or least-squares resampling (lsr)",
            "argstr": "--method={method}",
        },
    ),
    (
        "interp",
        ty.Any,
        {"help_string": "interpolation method", "argstr": "--interp={interp}"},
    ),
    (
        "datatype",
        ty.Any,
        {"help_string": "force output data type", "argstr": "-d={datatype}"},
    ),
]
ApplyTOPUP_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
ApplyTOPUP_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ApplyTOPUP(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage.nifti import Nifti1
    >>> from fileformats.medimage.nifti import NiftiGz
    >>> from fileformats.text import TextFile
    >>> from pydra.tasks.fsl.auto.apply_topup import ApplyTOPUP

    >>> task = ApplyTOPUP()
    >>> task.inputs.in_files = [Nifti1.mock("epi.nii"), Nifti1.mock("epi_rev.nii")]
    >>> task.inputs.encoding_file = TextFile.mock("topup_encoding.txt")
    >>> task.inputs.in_topup_fieldcoef = NiftiGz.mock("topup_fieldcoef.nii.gz")
    >>> task.inputs.in_topup_movpar = TextFile.mock("topup_movpar.txt")
    >>> task.cmdline
    'applytopup --datain=topup_encoding.txt --imain=epi.nii,epi_rev.nii --inindex=1,2 --topup=topup --out=epi_corrected.nii.gz'


    """

    input_spec = ApplyTOPUP_input_spec
    output_spec = ApplyTOPUP_output_spec
    executable = "applytopup"
