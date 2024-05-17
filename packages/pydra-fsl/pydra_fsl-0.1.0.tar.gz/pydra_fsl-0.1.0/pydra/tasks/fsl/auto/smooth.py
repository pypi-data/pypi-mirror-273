from fileformats.medimage.nifti import Nifti1
from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs

input_fields = [
    (
        "in_file",
        Nifti1,
        {"help_string": "", "argstr": "{in_file}", "mandatory": True, "position": 0},
    ),
    (
        "sigma",
        float,
        {
            "help_string": "gaussian kernel sigma in mm (not voxels)",
            "argstr": "-kernel gauss {sigma:.03} -fmean",
            "mandatory": True,
            "position": 1,
            "xor": ["fwhm"],
        },
    ),
    (
        "fwhm",
        float,
        {
            "help_string": "gaussian kernel fwhm, will be converted to sigma in mm (not voxels)",
            "argstr": "-kernel gauss {fwhm:.03} -fmean",
            "mandatory": True,
            "position": 1,
            "xor": ["sigma"],
        },
    ),
    (
        "smoothed_file",
        Path,
        {
            "help_string": "",
            "argstr": "{smoothed_file}",
            "position": 2,
            "output_file_template": "{in_file}_smooth",
        },
    ),
]
Smooth_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Smooth_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Smooth(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage.nifti import Nifti1
    >>> from pydra.tasks.fsl.auto.smooth import Smooth

    >>> task = Smooth()
    >>> task.inputs.in_file = Nifti1.mock("functional2.nii")
    >>> task.inputs.sigma = 8.0
    >>> task.cmdline
    'fslmaths functional2.nii -kernel gauss 8.000 -fmean functional2_smooth.nii.gz'


    >>> task = Smooth()
    >>> task.inputs.in_file = Nifti1.mock("functional2.nii")
    >>> task.inputs.fwhm = 8.0
    >>> task.cmdline
    'fslmaths functional2.nii -kernel gauss 3.397 -fmean functional2_smooth.nii.gz'


    >>> task = Smooth()
    >>> task.inputs.in_file = Nifti1.mock("functional2.nii")
    >>> task.cmdline
    'None'


    """

    input_spec = Smooth_input_spec
    output_spec = Smooth_output_spec
    executable = "fslmaths"
