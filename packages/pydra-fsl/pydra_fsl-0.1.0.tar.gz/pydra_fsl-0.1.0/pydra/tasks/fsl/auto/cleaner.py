from fileformats.generic.file import File
from pydra.engine import ShellCommandTask
from pydra.engine import specs

input_fields = [
    (
        "artifacts_list_file",
        File,
        {
            "help_string": "Text file listing which ICs are artifacts; can be the output from classification or can be created manually",
            "argstr": "{artifacts_list_file}",
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "cleanup_motion",
        bool,
        {
            "help_string": "cleanup motion confounds, looks for design.fsf for highpass filter cut-off",
            "argstr": "-m",
            "position": 2,
        },
    ),
    (
        "highpass",
        float,
        100,
        {
            "help_string": "cleanup motion confounds",
            "argstr": "-m -h {highpass}",
            "position": 2,
        },
    ),
    (
        "aggressive",
        bool,
        {
            "help_string": "Apply aggressive (full variance) cleanup, instead of the default less-aggressive (unique variance) cleanup.",
            "argstr": "-A",
            "position": 3,
        },
    ),
    (
        "confound_file",
        File,
        {
            "help_string": "Include additional confound file.",
            "argstr": "-x {confound_file}",
            "position": 4,
        },
    ),
    (
        "confound_file_1",
        File,
        {
            "help_string": "Include additional confound file.",
            "argstr": "-x {confound_file_1}",
            "position": 5,
        },
    ),
    (
        "confound_file_2",
        File,
        {
            "help_string": "Include additional confound file.",
            "argstr": "-x {confound_file_2}",
            "position": 6,
        },
    ),
]
Cleaner_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("cleaned_functional_file", File, {"help_string": "Cleaned session data"})
]
Cleaner_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Cleaner(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from pydra.tasks.fsl.auto.cleaner import Cleaner

    """

    input_spec = Cleaner_input_spec
    output_spec = Cleaner_output_spec
    executable = "fix -a"
