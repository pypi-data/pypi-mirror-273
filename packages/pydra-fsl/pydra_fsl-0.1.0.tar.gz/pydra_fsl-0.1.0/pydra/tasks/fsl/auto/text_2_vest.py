from fileformats.datascience.data import TextMatrix
from fileformats.text import TextFile
from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs

input_fields = [
    (
        "in_file",
        TextFile,
        {
            "help_string": "plain text file representing your design, contrast, or f-test matrix",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "file name to store matrix data in the format used by FSL tools (e.g., design.mat, design.con design.fts)",
            "argstr": "{out_file}",
            "mandatory": True,
            "position": 1,
        },
    ),
]
Text2Vest_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "out_file",
        TextMatrix,
        {"help_string": "matrix data in the format used by FSL tools"},
    )
]
Text2Vest_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Text2Vest(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.datascience.data import TextMatrix
    >>> from fileformats.text import TextFile
    >>> from pydra.tasks.fsl.auto.text_2_vest import Text2Vest

    >>> task = Text2Vest()
    >>> task.inputs.in_file = TextFile.mock("design.txt")
    >>> task.inputs.out_file = "design.mat"
    >>> task.cmdline
    'Text2Vest design.txt design.mat'


    """

    input_spec = Text2Vest_input_spec
    output_spec = Text2Vest_output_spec
    executable = "Text2Vest"
