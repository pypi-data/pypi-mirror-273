from fileformats.medimage.nifti import Nifti1
from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs
import typing as ty

input_fields = [
    (
        "dimension",
        ty.Any,
        "T",
        {
            "help_string": "dimension to percentile across",
            "argstr": "-{dimension}perc",
            "position": 4,
        },
    ),
    (
        "perc",
        ty.Any,
        {
            "help_string": "nth percentile (0-100) of FULL RANGE across dimension",
            "argstr": "{perc}",
            "position": 5,
        },
    ),
    (
        "in_file",
        Nifti1,
        {
            "help_string": "image to operate on",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": 2,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "image to write",
            "argstr": "{out_file}",
            "position": -2,
            "output_file_template": "out_file",
        },
    ),
    (
        "internal_datatype",
        ty.Any,
        {
            "help_string": "datatype to use for calculations (default is float)",
            "argstr": "-dt {internal_datatype}",
            "position": 1,
        },
    ),
    (
        "output_datatype",
        ty.Any,
        {
            "help_string": "datatype to use for output (default uses input type)",
            "argstr": "-odt {output_datatype}",
            "position": -1,
        },
    ),
    (
        "nan2zeros",
        bool,
        {
            "help_string": "change NaNs to zeros before doing anything",
            "argstr": "-nan",
            "position": 3,
        },
    ),
]
PercentileImage_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
PercentileImage_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class PercentileImage(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage.nifti import Nifti1
    >>> from pydra.tasks.fsl.auto.percentile_image import PercentileImage

    >>> task = PercentileImage()
    >>> task.inputs.in_file = Nifti1.mock("functional.nii"  # doctest: +SKIP)
    >>> task.cmdline
    'fslmaths functional.nii -Tperc 90 functional_perc.nii'


    """

    input_spec = PercentileImage_input_spec
    output_spec = PercentileImage_output_spec
    executable = "fslmaths"
