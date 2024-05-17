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
            "help_string": "filtering operation to perform in dilation",
            "argstr": "-dil{operation}",
            "mandatory": True,
            "position": 6,
        },
    ),
    (
        "kernel_shape",
        ty.Any,
        {
            "help_string": "kernel shape to use",
            "argstr": "-kernel {kernel_shape}",
            "position": 4,
        },
    ),
    (
        "kernel_size",
        float,
        {
            "help_string": "kernel size - voxels for box/boxv, mm for sphere, mm sigma for gauss",
            "argstr": "{kernel_size:.4}",
            "position": 5,
            "xor": ["kernel_file"],
        },
    ),
    (
        "kernel_file",
        File,
        {
            "help_string": "use external file for kernel",
            "argstr": "{kernel_file}",
            "position": 5,
            "xor": ["kernel_size"],
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
DilateImage_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
DilateImage_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class DilateImage(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from pydra.tasks.fsl.auto.dilate_image import DilateImage

    """

    input_spec = DilateImage_input_spec
    output_spec = DilateImage_output_spec
    executable = "fslmaths"
