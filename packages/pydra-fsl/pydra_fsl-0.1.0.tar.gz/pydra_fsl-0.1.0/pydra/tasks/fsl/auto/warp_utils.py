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
            "help_string": "Name of file containing warp-coefficients/fields. This would typically be the output from the --cout switch of fnirt (but can also use fields, like the output from --fout).",
            "argstr": "--in={in_file}",
            "mandatory": True,
        },
    ),
    (
        "reference",
        Nifti1,
        {
            "help_string": "Name of a file in target space. Note that the target space is now different from the target space that was used to create the --warp file. It would typically be the file that was specified with the --in argument when running fnirt.",
            "argstr": "--ref={reference}",
            "mandatory": True,
        },
    ),
    (
        "out_format",
        ty.Any,
        {
            "help_string": "Specifies the output format. If set to field (default) the output will be a (4D) field-file. If set to spline the format will be a (4D) file of spline coefficients.",
            "argstr": "--outformat={out_format}",
        },
    ),
    (
        "warp_resolution",
        ty.Any,
        {
            "help_string": "Specifies the resolution/knot-spacing of the splines pertaining to the coefficients in the --out file. This parameter is only relevant if --outformat is set to spline. It should be noted that if the --in file has a higher resolution, the resulting coefficients will pertain to the closest (in a least-squares sense) file in the space of fields with the --warpres resolution. It should also be noted that the resolution will always be an integer multiple of the voxel size.",
            "argstr": "--warpres={warp_resolution[0]:0.4},{warp_resolution[1]:0.4},{warp_resolution[2]:0.4}",
        },
    ),
    (
        "knot_space",
        ty.Any,
        {
            "help_string": "Alternative (to --warpres) specification of the resolution of the output spline-field.",
            "argstr": "--knotspace={knot_space[0]},{knot_space[1]},{knot_space[2]}",
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "Name of output file. The format of the output depends on what other parameters are set. The default format is a (4D) field-file. If the --outformat is set to spline the format will be a (4D) file of spline coefficients.",
            "argstr": "--out={out_file}",
            "position": -1,
        },
    ),
    (
        "write_jacobian",
        bool,
        {
            "help_string": "Switch on --jac flag with automatically generated filename",
            "mandatory": True,
        },
    ),
    (
        "out_jacobian",
        Path,
        {
            "help_string": "Specifies that a (3D) file of Jacobian determinants corresponding to --in should be produced and written to filename.",
            "argstr": "--jac={out_jacobian}",
        },
    ),
    (
        "with_affine",
        bool,
        {
            "help_string": "Specifies that the affine transform (i.e. that which was specified for the --aff parameter in fnirt) should be included as displacements in the --out file. That can be useful for interfacing with software that cannot decode FSL/fnirt coefficient-files (where the affine transform is stored separately from the displacements).",
            "argstr": "--withaff",
        },
    ),
]
WarpUtils_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "out_file",
        File,
        {
            "help_string": "Name of output file, containing the warp as field or coefficients."
        },
    ),
    (
        "out_jacobian",
        File,
        {
            "help_string": "Name of output file, containing the map of the determinant of the Jacobian"
        },
    ),
]
WarpUtils_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class WarpUtils(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from fileformats.medimage.nifti import Nifti1
    >>> from pydra.tasks.fsl.auto.warp_utils import WarpUtils

    >>> task = WarpUtils()
    >>> task.inputs.in_file = Nifti1.mock("warpfield.nii")
    >>> task.inputs.reference = Nifti1.mock("T1.nii")
    >>> task.inputs.out_format = "spline"
    >>> task.inputs.warp_resolution = (10,10,10)
    >>> task.cmdline
    'fnirtfileutils --in=warpfield.nii --outformat=spline --ref=T1.nii --warpres=10.0000,10.0000,10.0000 --out=warpfield_coeffs.nii.gz'


    """

    input_spec = WarpUtils_input_spec
    output_spec = WarpUtils_output_spec
    executable = "fnirtfileutils"
