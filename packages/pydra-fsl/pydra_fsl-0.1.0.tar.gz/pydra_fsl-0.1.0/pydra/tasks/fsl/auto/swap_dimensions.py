from fileformats.generic.file import File
from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs
import typing as ty

input_fields = [
    (
        "in_file",
        File,
        {
            "help_string": "input image",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": "1",
        },
    ),
    (
        "new_dims",
        ty.Any,
        {
            "help_string": "3-tuple of new dimension order",
            "argstr": "{new_dims[0]} {new_dims[1]} {new_dims[2]}",
            "mandatory": True,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "image to write",
            "argstr": "{out_file}",
            "output_file_template": "out_file",
        },
    ),
]
SwapDimensions_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
SwapDimensions_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class SwapDimensions(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from pydra.tasks.fsl.auto.swap_dimensions import SwapDimensions

    """

    input_spec = SwapDimensions_input_spec
    output_spec = SwapDimensions_output_spec
    executable = "fslswapdim"
