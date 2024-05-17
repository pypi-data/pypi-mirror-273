from fileformats.generic.file import File
from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs
import typing as ty

input_fields = [
    (
        "in_file",
        ty.Any,
        {
            "help_string": "file or list of files with columns of timecourse information",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "plot_start",
        int,
        {
            "help_string": "first column from in-file to plot",
            "argstr": "--start={plot_start}",
            "xor": ("plot_range",),
        },
    ),
    (
        "plot_finish",
        int,
        {
            "help_string": "final column from in-file to plot",
            "argstr": "--finish={plot_finish}",
            "xor": ("plot_range",),
        },
    ),
    (
        "plot_range",
        ty.Any,
        {
            "help_string": "first and last columns from the in-file to plot",
            "argstr": "{plot_range}",
            "xor": ("plot_start", "plot_finish"),
        },
    ),
    ("title", str, {"help_string": "plot title", "argstr": "{title}"}),
    (
        "legend_file",
        File,
        {"help_string": "legend file", "argstr": "--legend={legend_file}"},
    ),
    (
        "labels",
        ty.Any,
        {"help_string": "label or list of labels", "argstr": "{labels}"},
    ),
    (
        "y_min",
        float,
        {
            "help_string": "minimum y value",
            "argstr": "--ymin={y_min:.2}",
            "xor": ("y_range",),
        },
    ),
    (
        "y_max",
        float,
        {
            "help_string": "maximum y value",
            "argstr": "--ymax={y_max:.2}",
            "xor": ("y_range",),
        },
    ),
    (
        "y_range",
        ty.Any,
        {
            "help_string": "min and max y axis values",
            "argstr": "{y_range}",
            "xor": ("y_min", "y_max"),
        },
    ),
    (
        "x_units",
        int,
        1,
        {
            "help_string": "scaling units for x-axis (between 1 and length of in file)",
            "argstr": "-u {x_units}",
        },
    ),
    (
        "plot_size",
        ty.Any,
        {"help_string": "plot image height and width", "argstr": "{plot_size}"},
    ),
    (
        "x_precision",
        int,
        {
            "help_string": "precision of x-axis labels",
            "argstr": "--precision={x_precision}",
        },
    ),
    (
        "sci_notation",
        bool,
        {"help_string": "switch on scientific notation", "argstr": "--sci"},
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
PlotTimeSeries_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
PlotTimeSeries_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class PlotTimeSeries(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from pydra.tasks.fsl.auto.plot_time_series import PlotTimeSeries

    """

    input_spec = PlotTimeSeries_input_spec
    output_spec = PlotTimeSeries_output_spec
    executable = "fsl_tsplot"
