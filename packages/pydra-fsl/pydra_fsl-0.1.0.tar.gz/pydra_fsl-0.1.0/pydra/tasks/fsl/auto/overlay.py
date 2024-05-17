from fileformats.generic.file import File
from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs
import typing as ty

input_fields = [
    (
        "transparency",
        bool,
        True,
        {
            "help_string": "make overlay colors semi-transparent",
            "argstr": "{transparency}",
            "position": 1,
        },
    ),
    (
        "out_type",
        ty.Any,
        "float",
        {
            "help_string": "write output with float or int",
            "argstr": "{out_type}",
            "position": 2,
        },
    ),
    (
        "use_checkerboard",
        bool,
        {
            "help_string": "use checkerboard mask for overlay",
            "argstr": "-c",
            "position": 3,
        },
    ),
    (
        "background_image",
        File,
        {
            "help_string": "image to use as background",
            "argstr": "{background_image}",
            "mandatory": True,
            "position": 4,
        },
    ),
    (
        "auto_thresh_bg",
        bool,
        {
            "help_string": "automatically threshold the background image",
            "argstr": "-a",
            "mandatory": True,
            "position": 5,
            "xor": ("auto_thresh_bg", "full_bg_range", "bg_thresh"),
        },
    ),
    (
        "full_bg_range",
        bool,
        {
            "help_string": "use full range of background image",
            "argstr": "-A",
            "mandatory": True,
            "position": 5,
            "xor": ("auto_thresh_bg", "full_bg_range", "bg_thresh"),
        },
    ),
    (
        "bg_thresh",
        ty.Any,
        {
            "help_string": "min and max values for background intensity",
            "argstr": "{bg_thresh[0]:.3} {bg_thresh[1]:.3}",
            "mandatory": True,
            "position": 5,
            "xor": ("auto_thresh_bg", "full_bg_range", "bg_thresh"),
        },
    ),
    (
        "stat_image",
        File,
        {
            "help_string": "statistical image to overlay in color",
            "argstr": "{stat_image}",
            "mandatory": True,
            "position": 6,
        },
    ),
    (
        "stat_thresh",
        ty.Any,
        {
            "help_string": "min and max values for the statistical overlay",
            "argstr": "{stat_thresh[0]:.2} {stat_thresh[1]:.2}",
            "mandatory": True,
            "position": 7,
        },
    ),
    (
        "show_negative_stats",
        bool,
        {
            "help_string": "display negative statistics in overlay",
            "argstr": "{show_negative_stats}",
            "position": 8,
            "xor": ["stat_image2"],
        },
    ),
    (
        "stat_image2",
        File,
        {
            "help_string": "second statistical image to overlay in color",
            "argstr": "{stat_image2}",
            "position": 9,
            "xor": ["show_negative_stats"],
        },
    ),
    (
        "stat_thresh2",
        ty.Any,
        {
            "help_string": "min and max values for second statistical overlay",
            "argstr": "{stat_thresh2[0]:.2} {stat_thresh2[1]:.2}",
            "position": 10,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "combined image volume",
            "argstr": "{out_file}",
            "position": -1,
            "output_file_template": "out_file",
        },
    ),
]
Overlay_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Overlay_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Overlay(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from pydra.tasks.fsl.auto.overlay import Overlay

    """

    input_spec = Overlay_input_spec
    output_spec = Overlay_output_spec
    executable = "overlay"
