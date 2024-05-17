from fileformats.generic.directory import Directory
from fileformats.generic.file import File
from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs

input_fields = [
    (
        "mel_ica",
        Directory,
        {
            "help_string": "Melodic output directory or directories",
            "argstr": "{mel_ica}",
            "copyfile": False,
            "position": 1,
        },
    ),
    (
        "trained_wts_file",
        File,
        {
            "help_string": "trained-weights file",
            "argstr": "{trained_wts_file}",
            "copyfile": False,
            "mandatory": True,
            "position": 2,
        },
    ),
    (
        "thresh",
        int,
        {
            "help_string": "Threshold for cleanup.",
            "argstr": "{thresh}",
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "artifacts_list_file",
        Path,
        {
            "help_string": "Text file listing which ICs are artifacts; can be the output from classification or can be created manually"
        },
    ),
]
Classifier_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "artifacts_list_file",
        File,
        {
            "help_string": "Text file listing which ICs are artifacts; can be the output from classification or can be created manually"
        },
    )
]
Classifier_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Classifier(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.directory import Directory
    >>> from fileformats.generic.file import File
    >>> from pydra.tasks.fsl.auto.classifier import Classifier

    """

    input_spec = Classifier_input_spec
    output_spec = Classifier_output_spec
    executable = "fix -c"
