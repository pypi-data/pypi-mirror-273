from fileformats.generic.directory import Directory
from fileformats.generic.file import File
from pydra.engine import ShellCommandTask
from pydra.engine import specs

input_fields = [
    (
        "fsf_file",
        File,
        {
            "help_string": "File specifying the feat design spec file",
            "argstr": "{fsf_file}",
            "mandatory": True,
            "position": 0,
        },
    )
]
FEAT_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("feat_dir", Directory, {})]
FEAT_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class FEAT(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.directory import Directory
    >>> from fileformats.generic.file import File
    >>> from pydra.tasks.fsl.auto.feat import FEAT

    """

    input_spec = FEAT_input_spec
    output_spec = FEAT_output_spec
    executable = "feat"
