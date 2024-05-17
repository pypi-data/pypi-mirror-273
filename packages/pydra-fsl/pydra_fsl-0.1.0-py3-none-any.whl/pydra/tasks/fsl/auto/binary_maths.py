from fileformats.generic.file import File
from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs
import typing as ty

input_fields = [
    (
        "operation",
        ty.Any,
        {
            "help_string": "operation to perform",
            "argstr": "-{operation}",
            "mandatory": True,
            "position": 4,
        },
    ),
    (
        "operand_file",
        File,
        {
            "help_string": "second image to perform operation with",
            "argstr": "{operand_file}",
            "mandatory": True,
            "position": 5,
            "xor": ["operand_value"],
        },
    ),
    (
        "operand_value",
        float,
        {
            "help_string": "value to perform operation with",
            "argstr": "{operand_value:.8}",
            "mandatory": True,
            "position": 5,
            "xor": ["operand_file"],
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
BinaryMaths_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
BinaryMaths_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class BinaryMaths(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from pydra.tasks.fsl.auto.binary_maths import BinaryMaths

    """

    input_spec = BinaryMaths_input_spec
    output_spec = BinaryMaths_output_spec
    executable = "fslmaths"
