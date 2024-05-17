from fileformats.medimage.nifti import Nifti1
from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs
import typing as ty

input_fields = [
    (
        "op_string",
        ty.Any,
        {
            "help_string": "python formatted string of operations to perform",
            "argstr": "{op_string}",
            "mandatory": True,
            "position": 4,
        },
    ),
    (
        "operand_files",
        ty.List[Nifti1],
        {"help_string": "list of file names to plug into op string", "mandatory": True},
    ),
    (
        "in_file",
        Nifti1,
        {
            "help_string": "image to operate on",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": 2,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "image to write",
            "argstr": "{out_file}",
            "position": -2,
            "output_file_template": '"functional4.nii"',
        },
    ),
    (
        "internal_datatype",
        ty.Any,
        {
            "help_string": "datatype to use for calculations (default is float)",
            "argstr": "-dt {internal_datatype}",
            "position": 1,
        },
    ),
    (
        "output_datatype",
        ty.Any,
        {
            "help_string": "datatype to use for output (default uses input type)",
            "argstr": "-odt {output_datatype}",
            "position": -1,
        },
    ),
    (
        "nan2zeros",
        bool,
        {
            "help_string": "change NaNs to zeros before doing anything",
            "argstr": "-nan",
            "position": 3,
        },
    ),
]
MultiImageMaths_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
MultiImageMaths_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class MultiImageMaths(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage.nifti import Nifti1
    >>> from pydra.tasks.fsl.auto.multi_image_maths import MultiImageMaths

    >>> task = MultiImageMaths()
    >>> task.inputs.op_string = "-add %s -mul -1 -div %s"
    >>> task.inputs.operand_files = [Nifti1.mock("functional2.nii"), Nifti1.mock("functional3.nii")]
    >>> task.inputs.in_file = Nifti1.mock("functional.nii")
    >>> task.inputs.out_file = "functional4.nii"
    >>> task.cmdline
    'fslmaths functional.nii -add functional2.nii -mul -1 -div functional3.nii functional4.nii'


    """

    input_spec = MultiImageMaths_input_spec
    output_spec = MultiImageMaths_output_spec
    executable = "fslmaths"
