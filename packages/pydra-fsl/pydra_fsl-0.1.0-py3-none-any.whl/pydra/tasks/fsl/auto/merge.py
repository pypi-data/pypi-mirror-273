from fileformats.medimage.nifti import Nifti1
from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs
import typing as ty

input_fields = [
    (
        "in_files",
        ty.List[Nifti1],
        {"help_string": "", "argstr": "{in_files}", "mandatory": True, "position": 2},
    ),
    (
        "dimension",
        ty.Any,
        {
            "help_string": "dimension along which to merge, optionally set tr input when dimension is t",
            "argstr": "-{dimension}",
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "tr",
        float,
        {
            "help_string": "use to specify TR in seconds (default is 1.00 sec), overrides dimension and sets it to tr",
            "argstr": "{tr:.2}",
            "position": -1,
        },
    ),
    (
        "merged_file",
        Path,
        {
            "help_string": "",
            "argstr": "{merged_file}",
            "position": 1,
            "output_file_template": "{in_files}_merged",
        },
    ),
]
Merge_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Merge_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Merge(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage.nifti import Nifti1
    >>> from pydra.tasks.fsl.auto.merge import Merge

    >>> task = Merge()
    >>> task.inputs.in_files = [Nifti1.mock("functional2.nii"), Nifti1.mock("functional3.nii")]
    >>> task.inputs.dimension = "t"
    >>> task.inputs.tr = 2.25
    >>> task.cmdline
    'fslmerge -tr functional2_merged.nii.gz functional2.nii functional3.nii 2.25'


    """

    input_spec = Merge_input_spec
    output_spec = Merge_output_spec
    executable = "fslmerge"
