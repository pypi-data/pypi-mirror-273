from fileformats.generic.file import File
from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs

input_fields = [
    (
        "in_file",
        File,
        {
            "help_string": "source image",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "dest_file",
        Path,
        {
            "help_string": "destination image",
            "argstr": "{dest_file}",
            "copyfile": True,
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "ignore_dims",
        bool,
        {
            "help_string": "Do not copy image dimensions",
            "argstr": "-d",
            "position": "-1",
        },
    ),
]
CopyGeom_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("out_file", File, {"help_string": "image with new geometry header"})]
CopyGeom_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class CopyGeom(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from pydra.tasks.fsl.auto.copy_geom import CopyGeom

    """

    input_spec = CopyGeom_input_spec
    output_spec = CopyGeom_output_spec
    executable = "fslcpgeom"
