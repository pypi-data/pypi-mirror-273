from fileformats.generic.file import File
from fileformats.medimage.nifti import Nifti1
from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs
import typing as ty

input_fields = [
    (
        "scanner",
        ty.Any,
        "SIEMENS",
        {"help_string": "must be SIEMENS", "argstr": "{scanner}", "position": 1},
    ),
    (
        "in_phase",
        Nifti1,
        {
            "help_string": "Phase difference map, in SIEMENS format range from 0-4096 or 0-8192)",
            "argstr": "{in_phase}",
            "mandatory": True,
            "position": 2,
        },
    ),
    (
        "in_magnitude",
        Nifti1,
        {
            "help_string": "Magnitude difference map, brain extracted",
            "argstr": "{in_magnitude}",
            "mandatory": True,
            "position": 3,
        },
    ),
    (
        "delta_TE",
        float,
        {
            "help_string": "echo time difference of the fieldmap sequence in ms. (usually 2.46ms in Siemens)",
            "argstr": "{delta_TE}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "nocheck",
        bool,
        False,
        {
            "help_string": "do not perform sanity checks for image size/range/dimensions",
            "argstr": "--nocheck",
            "position": -1,
        },
    ),
    (
        "out_fieldmap",
        Path,
        {
            "help_string": "output name for prepared fieldmap",
            "argstr": "{out_fieldmap}",
            "position": 4,
        },
    ),
]
PrepareFieldmap_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("out_fieldmap", File, {"help_string": "output name for prepared fieldmap"})
]
PrepareFieldmap_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class PrepareFieldmap(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from fileformats.medimage.nifti import Nifti1
    >>> from pydra.tasks.fsl.auto.prepare_fieldmap import PrepareFieldmap

    >>> task = PrepareFieldmap()
    >>> task.inputs.in_phase = Nifti1.mock("phase.nii")
    >>> task.inputs.in_magnitude = Nifti1.mock("magnitude.nii")
    >>> task.cmdline
    'fsl_prepare_fieldmap SIEMENS phase.nii magnitude.nii .../phase_fslprepared.nii.gz 2.460000'


    """

    input_spec = PrepareFieldmap_input_spec
    output_spec = PrepareFieldmap_output_spec
    executable = "fsl_prepare_fieldmap"
