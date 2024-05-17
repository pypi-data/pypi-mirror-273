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
            "help_string": "input volume",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "image_edges",
        File,
        {
            "help_string": "volume to display edge overlay for (useful for checking registration",
            "argstr": "{image_edges}",
            "position": 2,
        },
    ),
    (
        "label_slices",
        bool,
        True,
        {"help_string": "display slice number", "argstr": "-L", "position": 3},
    ),
    (
        "colour_map",
        File,
        {
            "help_string": "use different colour map from that stored in nifti header",
            "argstr": "-l {colour_map}",
            "position": 4,
        },
    ),
    (
        "intensity_range",
        ty.Any,
        {
            "help_string": "min and max intensities to display",
            "argstr": "-i {intensity_range[0]:.3} {intensity_range[1]:.3}",
            "position": 5,
        },
    ),
    (
        "threshold_edges",
        float,
        {
            "help_string": "use threshold for edges",
            "argstr": "-e {threshold_edges:.3}",
            "position": 6,
        },
    ),
    (
        "dither_edges",
        bool,
        {
            "help_string": "produce semi-transparent (dithered) edges",
            "argstr": "-t",
            "position": 7,
        },
    ),
    (
        "nearest_neighbour",
        bool,
        {
            "help_string": "use nearest neighbor interpolation for output",
            "argstr": "-n",
            "position": 8,
        },
    ),
    (
        "show_orientation",
        bool,
        True,
        {
            "help_string": "label left-right orientation",
            "argstr": "{show_orientation}",
            "position": 9,
        },
    ),
    (
        "single_slice",
        ty.Any,
        {
            "help_string": "output picture of single slice in the x, y, or z plane",
            "argstr": "-{single_slice}",
            "position": 10,
            "requires": ["slice_number"],
            "xor": ("single_slice", "middle_slices", "all_axial", "sample_axial"),
        },
    ),
    (
        "slice_number",
        int,
        {
            "help_string": "slice number to save in picture",
            "argstr": "-{slice_number}",
            "position": 11,
        },
    ),
    (
        "middle_slices",
        bool,
        {
            "help_string": "output picture of mid-sagittal, axial, and coronal slices",
            "argstr": "-a",
            "position": 10,
            "xor": ("single_slice", "middle_slices", "all_axial", "sample_axial"),
        },
    ),
    (
        "all_axial",
        bool,
        {
            "help_string": "output all axial slices into one picture",
            "argstr": "-A",
            "position": 10,
            "requires": ["image_width"],
            "xor": ("single_slice", "middle_slices", "all_axial", "sample_axial"),
        },
    ),
    (
        "sample_axial",
        int,
        {
            "help_string": "output every n axial slices into one picture",
            "argstr": "-S {sample_axial}",
            "position": 10,
            "requires": ["image_width"],
            "xor": ("single_slice", "middle_slices", "all_axial", "sample_axial"),
        },
    ),
    (
        "image_width",
        int,
        {"help_string": "max picture width", "argstr": "{image_width}", "position": -2},
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "picture to write",
            "argstr": "{out_file}",
            "position": -1,
            "output_file_template": "out_file",
        },
    ),
    (
        "scaling",
        float,
        {"help_string": "image scale", "argstr": "-s {scaling}", "position": 0},
    ),
]
Slicer_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Slicer_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Slicer(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from pydra.tasks.fsl.auto.slicer import Slicer

    """

    input_spec = Slicer_input_spec
    output_spec = Slicer_output_spec
    executable = "slicer"
