from fileformats.datascience.data import TextMatrix
from fileformats.generic.file import File
from fileformats.medimage.nifti import Nifti1
from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs
import typing as ty

input_fields = [
    (
        "in_file",
        Nifti1,
        {
            "help_string": "filename for input vector or tensor field",
            "argstr": "-i {in_file}",
            "mandatory": True,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "filename for output registered vector or tensor field",
            "argstr": "-o {out_file}",
            "output_file_template": '"diffusion_vreg.nii"',
        },
    ),
    (
        "ref_vol",
        Nifti1,
        {
            "help_string": "filename for reference (target) volume",
            "argstr": "-r {ref_vol}",
            "mandatory": True,
        },
    ),
    (
        "affine_mat",
        TextMatrix,
        {
            "help_string": "filename for affine transformation matrix",
            "argstr": "-t {affine_mat}",
        },
    ),
    (
        "warp_field",
        File,
        {
            "help_string": "filename for 4D warp field for nonlinear registration",
            "argstr": "-w {warp_field}",
        },
    ),
    (
        "rotation_mat",
        File,
        {
            "help_string": "filename for secondary affine matrix if set, this will be used for the rotation of the vector/tensor field",
            "argstr": "--rotmat={rotation_mat}",
        },
    ),
    (
        "rotation_warp",
        File,
        {
            "help_string": "filename for secondary warp field if set, this will be used for the rotation of the vector/tensor field",
            "argstr": "--rotwarp={rotation_warp}",
        },
    ),
    (
        "interpolation",
        ty.Any,
        {
            "help_string": "interpolation method : nearestneighbour, trilinear (default), sinc or spline",
            "argstr": "--interp={interpolation}",
        },
    ),
    ("mask", File, {"help_string": "brain mask in input space", "argstr": "-m {mask}"}),
    (
        "ref_mask",
        File,
        {
            "help_string": "brain mask in output space (useful for speed up of nonlinear reg)",
            "argstr": "--refmask={ref_mask}",
        },
    ),
]
VecReg_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
VecReg_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class VecReg(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.datascience.data import TextMatrix
    >>> from fileformats.generic.file import File
    >>> from fileformats.medimage.nifti import Nifti1
    >>> from pydra.tasks.fsl.auto.vec_reg import VecReg

    >>> task = VecReg()
    >>> task.inputs.in_file = Nifti1.mock("diffusion.nii")
    >>> task.inputs.out_file = "diffusion_vreg.nii"
    >>> task.inputs.ref_vol = Nifti1.mock("mni.nii")
    >>> task.inputs.affine_mat = TextMatrix.mock("trans.mat")
    >>> task.inputs.warp_field = File.mock()
    >>> task.inputs.rotation_mat = File.mock()
    >>> task.inputs.rotation_warp = File.mock()
    >>> task.inputs.mask = File.mock()
    >>> task.inputs.ref_mask = File.mock()
    >>> task.cmdline
    'vecreg -t trans.mat -i diffusion.nii -o diffusion_vreg.nii -r mni.nii'


    """

    input_spec = VecReg_input_spec
    output_spec = VecReg_output_spec
    executable = "vecreg"
