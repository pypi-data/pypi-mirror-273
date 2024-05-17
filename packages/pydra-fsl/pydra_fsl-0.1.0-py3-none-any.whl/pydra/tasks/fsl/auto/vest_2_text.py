from fileformats.datascience.data import TextMatrix
from fileformats.generic.file import File
from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs

input_fields = [
    (
        "in_file",
        TextMatrix,
        {
            "help_string": "matrix data stored in the format used by FSL tools",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "out_file",
        Path,
        "design.txt",
        {
            "help_string": "file name to store text output from matrix",
            "argstr": "{out_file}",
            "position": 1,
        },
    ),
]
Vest2Text_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("out_file", File, {"help_string": "plain text representation of FSL matrix"})
]
Vest2Text_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Vest2Text(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.datascience.data import TextMatrix
    >>> from fileformats.generic.file import File
    >>> from pydra.tasks.fsl.auto.vest_2_text import Vest2Text

    >>> task = Vest2Text()
    >>> task.inputs.in_file = TextMatrix.mock("design.mat")
    >>> task.cmdline
    'Vest2Text design.mat design.txt'


    """

    input_spec = Vest2Text_input_spec
    output_spec = Vest2Text_output_spec
    executable = "Vest2Text"
