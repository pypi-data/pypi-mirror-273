from fileformats.generic.file import File
from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs
import typing as ty

input_fields = [
    (
        "thresh",
        float,
        {
            "help_string": "threshold value",
            "argstr": "{thresh}",
            "mandatory": True,
            "position": 4,
        },
    ),
    (
        "direction",
        ty.Any,
        "below",
        {"help_string": "zero-out either below or above thresh value"},
    ),
    (
        "use_robust_range",
        bool,
        {"help_string": "interpret thresh as percentage (0-100) of robust range"},
    ),
    (
        "use_nonzero_voxels",
        bool,
        {
            "help_string": "use nonzero voxels to calculate robust range",
            "requires": ["use_robust_range"],
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
Threshold_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Threshold_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Threshold(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from pydra.tasks.fsl.auto.threshold import Threshold

    """

    input_spec = Threshold_input_spec
    output_spec = Threshold_output_spec
    executable = "fslmaths"
