from fileformats.generic.file import File
from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs

input_fields = [
    (
        "in_file",
        File,
        {
            "help_string": "input filename",
            "argstr": "-i {in_file}",
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "out_roi",
        Path,
        {
            "help_string": "ROI volume output name",
            "argstr": "-r {out_roi}",
            "output_file_template": "{in_file}_ROI",
        },
    ),
    (
        "brainsize",
        int,
        {
            "help_string": "size of brain in z-dimension (default 170mm/150mm)",
            "argstr": "-b {brainsize}",
        },
    ),
    (
        "out_transform",
        Path,
        {
            "help_string": "Transformation matrix in_file to out_roi output name",
            "argstr": "-m {out_transform}",
            "output_file_template": "{in_file}_to_ROI",
        },
    ),
]
RobustFOV_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
RobustFOV_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class RobustFOV(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from pydra.tasks.fsl.auto.robust_fov import RobustFOV

    """

    input_spec = RobustFOV_input_spec
    output_spec = RobustFOV_output_spec
    executable = "robustfov"
