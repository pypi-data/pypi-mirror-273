from fileformats.generic.file import File
from pydra.engine import ShellCommandTask
from pydra.engine import specs
import typing as ty

input_fields = [
    (
        "mel_icas",
        ty.List[File],
        {
            "help_string": "Melodic output directories",
            "argstr": "{mel_icas}",
            "copyfile": False,
            "position": -1,
        },
    ),
    (
        "trained_wts_filestem",
        str,
        {
            "help_string": "trained-weights filestem, used for trained_wts_file and output directories",
            "argstr": "{trained_wts_filestem}",
            "position": 1,
        },
    ),
    (
        "loo",
        bool,
        {
            "help_string": "full leave-one-out test with classifier training",
            "argstr": "-l",
            "position": 2,
        },
    ),
]
Training_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("trained_wts_file", File, {"help_string": "Trained-weights file"})]
Training_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Training(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from pydra.tasks.fsl.auto.training import Training

    """

    input_spec = Training_input_spec
    output_spec = Training_output_spec
    executable = "fix -t"
