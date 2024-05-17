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
            "help_string": "input image (typically mean FA volume)",
            "argstr": "-i {in_file}",
            "mandatory": True,
        },
    ),
    (
        "project_data",
        bool,
        {
            "help_string": "project data onto skeleton",
            "argstr": "-p {project_data[0]:.3} {project_data[1]} {project_data[2]} {project_data[3]} {project_data[4]}",
            "requires": ["threshold", "distance_map", "data_file"],
        },
    ),
    ("threshold", float, {"help_string": "skeleton threshold value"}),
    ("distance_map", File, {"help_string": "distance map image"}),
    (
        "search_mask_file",
        File,
        {
            "help_string": "mask in which to use alternate search rule",
            "xor": ["use_cingulum_mask"],
        },
    ),
    (
        "use_cingulum_mask",
        bool,
        True,
        {
            "help_string": "perform alternate search using built-in cingulum mask",
            "xor": ["search_mask_file"],
        },
    ),
    (
        "data_file",
        File,
        {"help_string": "4D data to project onto skeleton (usually FA)"},
    ),
    (
        "alt_data_file",
        File,
        {
            "help_string": "4D non-FA data to project onto skeleton",
            "argstr": "-a {alt_data_file}",
        },
    ),
    (
        "alt_skeleton",
        File,
        {"help_string": "alternate skeleton to use", "argstr": "-s {alt_skeleton}"},
    ),
    ("projected_data", Path, {"help_string": "input data projected onto skeleton"}),
    (
        "skeleton_file",
        ty.Any,
        {"help_string": "write out skeleton image", "argstr": "-o {skeleton_file}"},
    ),
]
TractSkeleton_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("projected_data", File, {"help_string": "input data projected onto skeleton"}),
    ("skeleton_file", File, {"help_string": "tract skeleton image"}),
]
TractSkeleton_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class TractSkeleton(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from pydra.tasks.fsl.auto.tract_skeleton import TractSkeleton

    """

    input_spec = TractSkeleton_input_spec
    output_spec = TractSkeleton_output_spec
    executable = "tbss_skeleton"
