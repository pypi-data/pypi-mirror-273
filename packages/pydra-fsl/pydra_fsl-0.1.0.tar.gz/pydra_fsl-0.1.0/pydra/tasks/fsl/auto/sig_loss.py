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
            "help_string": "b0 fieldmap file",
            "argstr": "-i {in_file}",
            "mandatory": True,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "output signal loss estimate file",
            "argstr": "-s {out_file}",
            "output_file_template": "out_file",
        },
    ),
    ("mask_file", File, {"help_string": "brain mask file", "argstr": "-m {mask_file}"}),
    (
        "echo_time",
        float,
        {"help_string": "echo time in seconds", "argstr": "--te={echo_time}"},
    ),
    (
        "slice_direction",
        ty.Any,
        {"help_string": "slicing direction", "argstr": "-d {slice_direction}"},
    ),
]
SigLoss_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
SigLoss_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class SigLoss(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from pydra.tasks.fsl.auto.sig_loss import SigLoss

    """

    input_spec = SigLoss_input_spec
    output_spec = SigLoss_output_spec
    executable = "sigloss"
