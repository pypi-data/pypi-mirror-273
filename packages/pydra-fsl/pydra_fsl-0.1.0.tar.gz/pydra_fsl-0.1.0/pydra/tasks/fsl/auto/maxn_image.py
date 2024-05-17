from fileformats.generic.file import File
from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs
import typing as ty

input_fields = [
    (
        "dimension",
        ty.Any,
        "T",
        {
            "help_string": "dimension to index max across",
            "argstr": "-{dimension}maxn",
            "position": 4,
        },
    ),
    (
        "in_file",
        File,
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
            "output_file_template": "out_file",
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
MaxnImage_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
MaxnImage_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class MaxnImage(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from pydra.tasks.fsl.auto.maxn_image import MaxnImage

    """

    input_spec = MaxnImage_input_spec
    output_spec = MaxnImage_output_spec
    executable = "fslmaths"
