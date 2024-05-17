from fileformats.generic.directory import Directory
from fileformats.generic.file import File
from fileformats.medimage_fsl import MelodicIca
from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs
import typing as ty

input_fields = [
    (
        "mel_icas",
        ty.List[MelodicIca],
        {
            "help_string": "Melodic output directories",
            "argstr": "{mel_icas}",
            "copyfile": False,
            "mandatory": True,
            "position": 3,
        },
    ),
    (
        "trained_wts_file",
        File,
        {
            "help_string": "trained-weights file",
            "argstr": "{trained_wts_file}",
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "output_directory",
        Path,
        {
            "help_string": "Path to folder in which to store the results of the accuracy test.",
            "argstr": "{output_directory}",
            "mandatory": True,
            "position": 2,
        },
    ),
]
AccuracyTester_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "output_directory",
        Directory,
        {
            "help_string": "Path to folder in which to store the results of the accuracy test."
        },
    )
]
AccuracyTester_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class AccuracyTester(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.directory import Directory
    >>> from fileformats.generic.file import File
    >>> from fileformats.medimage_fsl import MelodicIca
    >>> from pydra.tasks.fsl.auto.accuracy_tester import AccuracyTester

    """

    input_spec = AccuracyTester_input_spec
    output_spec = AccuracyTester_output_spec
    executable = "fix -C"
