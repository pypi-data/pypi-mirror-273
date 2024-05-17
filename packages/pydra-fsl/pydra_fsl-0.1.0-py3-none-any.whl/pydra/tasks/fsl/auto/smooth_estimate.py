from fileformats.generic.file import File
from fileformats.medimage.nifti import Nifti1
from fileformats.medimage.nifti import NiftiGz
from pydra.engine import ShellCommandTask
from pydra.engine import specs


def dlh_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["dlh"]


def resels_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["resels"]


def volume_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["volume"]


input_fields = [
    (
        "dof",
        int,
        {
            "help_string": "number of degrees of freedom",
            "argstr": "--dof={dof}",
            "mandatory": True,
            "xor": ["zstat_file"],
        },
    ),
    (
        "mask_file",
        Nifti1,
        {
            "help_string": "brain mask volume",
            "argstr": "--mask={mask_file}",
            "mandatory": True,
        },
    ),
    (
        "residual_fit_file",
        File,
        {
            "help_string": "residual-fit image file",
            "argstr": "--res={residual_fit_file}",
            "requires": ["dof"],
        },
    ),
    (
        "zstat_file",
        NiftiGz,
        {
            "help_string": "zstat image file",
            "argstr": "--zstat={zstat_file}",
            "xor": ["dof"],
        },
    ),
]
SmoothEstimate_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "dlh",
        float,
        {
            "help_string": "smoothness estimate sqrt(det(Lambda))",
            "callable": "dlh_callable",
        },
    ),
    (
        "volume",
        int,
        {"help_string": "number of voxels in mask", "callable": "volume_callable"},
    ),
    (
        "resels",
        float,
        {
            "help_string": "volume of resel, in voxels, defined as FWHM_x * FWHM_y * FWHM_z",
            "callable": "resels_callable",
        },
    ),
]
SmoothEstimate_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class SmoothEstimate(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from fileformats.medimage.nifti import Nifti1
    >>> from fileformats.medimage.nifti import NiftiGz
    >>> from pydra.tasks.fsl.auto.smooth_estimate import SmoothEstimate

    >>> task = SmoothEstimate()
    >>> task.inputs.mask_file = Nifti1.mock("mask.nii")
    >>> task.inputs.residual_fit_file = File.mock()
    >>> task.inputs.zstat_file = NiftiGz.mock("zstat1.nii.gz")
    >>> task.cmdline
    'smoothest --mask=mask.nii --zstat=zstat1.nii.gz'


    """

    input_spec = SmoothEstimate_input_spec
    output_spec = SmoothEstimate_output_spec
    executable = "smoothest"
