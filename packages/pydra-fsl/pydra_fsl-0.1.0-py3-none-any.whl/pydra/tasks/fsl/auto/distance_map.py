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
            "help_string": "image to calculate distance values for",
            "argstr": "--in={in_file}",
            "mandatory": True,
        },
    ),
    (
        "mask_file",
        File,
        {
            "help_string": "binary mask to constrain calculations",
            "argstr": "--mask={mask_file}",
        },
    ),
    ("invert_input", bool, {"help_string": "invert input image", "argstr": "--invert"}),
    (
        "local_max_file",
        ty.Any,
        {
            "help_string": "write an image of the local maxima",
            "argstr": "--localmax={local_max_file}",
        },
    ),
    (
        "distance_map",
        Path,
        {
            "help_string": "distance map to write",
            "argstr": "--out={distance_map}",
            "output_file_template": "distance_map",
        },
    ),
]
DistanceMap_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("local_max_file", File, {"help_string": "image of local maxima"})]
DistanceMap_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class DistanceMap(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from pydra.tasks.fsl.auto.distance_map import DistanceMap

    """

    input_spec = DistanceMap_input_spec
    output_spec = DistanceMap_output_spec
    executable = "distancemap"
