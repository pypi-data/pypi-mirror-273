from fileformats.generic.file import File
from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs
import typing as ty

input_fields = [
    (
        "in_files",
        ty.List[File],
        {
            "help_string": "a list of input volumes or a singleMatrixFile",
            "argstr": "{in_files}",
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "file with the resulting segmentation",
            "argstr": "{out_file}",
            "position": 2,
            "output_file_template": '"biggestSegmentation"',
        },
    ),
]
FindTheBiggest_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
FindTheBiggest_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class FindTheBiggest(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from pydra.tasks.fsl.auto.find_the_biggest import FindTheBiggest

    >>> task = FindTheBiggest()
    >>> task.inputs.in_files = ldir
    >>> task.inputs.out_file = "biggestSegmentation"
    >>> task.cmdline
    'find_the_biggest seeds_to_M1.nii seeds_to_M2.nii biggestSegmentation'


    """

    input_spec = FindTheBiggest_input_spec
    output_spec = FindTheBiggest_output_spec
    executable = "find_the_biggest"
