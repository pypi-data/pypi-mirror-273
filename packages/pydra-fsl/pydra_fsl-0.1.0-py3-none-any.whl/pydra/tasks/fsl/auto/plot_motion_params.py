from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs
import typing as ty

input_fields = [
    (
        "in_file",
        ty.Any,
        {
            "help_string": "file with motion parameters",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "in_source",
        ty.Any,
        {
            "help_string": "which program generated the motion parameter file - fsl, spm",
            "mandatory": True,
        },
    ),
    (
        "plot_type",
        ty.Any,
        {
            "help_string": "which motion type to plot - rotations, translations, displacement",
            "argstr": "{plot_type}",
            "mandatory": True,
        },
    ),
    (
        "plot_size",
        ty.Any,
        {"help_string": "plot image height and width", "argstr": "{plot_size}"},
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "image to write",
            "argstr": "-o {out_file}",
            "output_file_template": "out_file",
        },
    ),
]
PlotMotionParams_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
PlotMotionParams_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class PlotMotionParams(ShellCommandTask):
    """
    Examples
    -------

    >>> from pydra.tasks.fsl.auto.plot_motion_params import PlotMotionParams

    """

    input_spec = PlotMotionParams_input_spec
    output_spec = PlotMotionParams_output_spec
    executable = "fsl_tsplot"
