from fileformats.medimage.contents.imaging.derivatives import Mask
from fileformats.medimage.nifti import NiftiGz
from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs
import typing as ty

input_fields = [
    (
        "mask_file",
        NiftiGz[Mask],
        {
            "help_string": "binary image defining mask space",
            "argstr": "-mas {mask_file}",
            "mandatory": True,
            "position": 4,
        },
    ),
    (
        "in_file",
        NiftiGz,
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
            "output_file_template": "out_file.nii.gz",
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
ApplyMask_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
ApplyMask_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ApplyMask(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage.contents.imaging.derivatives import Mask
    >>> from fileformats.medimage.nifti import NiftiGz
    >>> from pydra.tasks.fsl.auto.apply_mask import ApplyMask

    """

    input_spec = ApplyMask_input_spec
    output_spec = ApplyMask_output_spec
    executable = "fslmaths"
