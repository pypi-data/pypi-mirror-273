from fileformats.generic.file import File
from fileformats.medimage.nifti import Nifti1
from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs

input_fields = [
    (
        "in_file",
        Nifti1,
        {
            "help_string": "4D input file",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "out_file",
        Path,
        {"help_string": "4D output file", "argstr": "{out_file}", "position": 1},
    ),
    (
        "ref_num",
        int,
        {
            "help_string": "reference number",
            "argstr": "{ref_num}",
            "mandatory": True,
            "position": 2,
        },
    ),
]
EddyCorrect_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "eddy_corrected",
        File,
        {"help_string": "path/name of 4D eddy corrected output file"},
    )
]
EddyCorrect_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class EddyCorrect(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from fileformats.medimage.nifti import Nifti1
    >>> from pydra.tasks.fsl.auto.eddy_correct import EddyCorrect

    >>> task = EddyCorrect()
    >>> task.inputs.in_file = Nifti1.mock("diffusion.nii")
    >>> task.inputs.out_file = "diffusion_edc.nii"
    >>> task.inputs.ref_num = 0
    >>> task.cmdline
    'eddy_correct diffusion.nii diffusion_edc.nii 0'


    """

    input_spec = EddyCorrect_input_spec
    output_spec = EddyCorrect_output_spec
    executable = "eddy_correct"
