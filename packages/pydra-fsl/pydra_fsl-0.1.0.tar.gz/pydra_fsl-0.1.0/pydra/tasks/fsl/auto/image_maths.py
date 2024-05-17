from fileformats.generic.file import File
from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs
import typing as ty

input_fields = [
    (
        "in_file",
        File,
        {"help_string": "", "argstr": "{in_file}", "mandatory": True, "position": 1},
    ),
    ("in_file2", File, {"help_string": "", "argstr": "{in_file2}", "position": 3}),
    (
        "mask_file",
        File,
        {
            "help_string": "use (following image>0) to mask current image",
            "argstr": "-mas {mask_file}",
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "",
            "argstr": "{out_file}",
            "position": -2,
            "output_file_template": '"foo_maths.nii"',
        },
    ),
    (
        "op_string",
        str,
        {
            "help_string": "string defining the operation, i. e. -add",
            "argstr": "{op_string}",
            "position": 2,
        },
    ),
    ("suffix", str, {"help_string": "out_file suffix"}),
    (
        "out_data_type",
        ty.Any,
        {
            "help_string": "output datatype, one of (char, short, int, float, double, input)",
            "argstr": "-odt {out_data_type}",
            "position": -1,
        },
    ),
]
ImageMaths_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
ImageMaths_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ImageMaths(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from pydra.tasks.fsl.auto.image_maths import ImageMaths

    >>> task = ImageMaths()
    >>> task.inputs.in_file = File.mock(anatfile)
    >>> task.inputs.in_file2 = File.mock()
    >>> task.inputs.mask_file = File.mock()
    >>> task.inputs.out_file = "foo_maths.nii"
    >>> task.inputs.op_string = "-add 5"
    >>> task.cmdline
    'None'


    """

    input_spec = ImageMaths_input_spec
    output_spec = ImageMaths_output_spec
    executable = "fslmaths"
