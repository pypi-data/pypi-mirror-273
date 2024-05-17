from fileformats.generic.file import File
from fileformats.medimage.nifti import Nifti1
from fileformats.text import TextFile
from pydra.engine import ShellCommandTask
from pydra.engine import specs

input_fields = [
    (
        "img_file",
        Nifti1,
        {
            "help_string": "filename of a destination image",
            "argstr": "-img {img_file}",
            "mandatory": True,
        },
    ),
    (
        "std_file",
        Nifti1,
        {
            "help_string": "filename of the image in standard space",
            "argstr": "-std {std_file}",
            "mandatory": True,
        },
    ),
    (
        "in_coords",
        TextFile,
        {
            "help_string": "filename of file containing coordinates",
            "argstr": "{in_coords}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "xfm_file",
        File,
        {
            "help_string": "filename of affine transform (e.g. source2dest.mat)",
            "argstr": "-xfm {xfm_file}",
            "xor": ["warp_file"],
        },
    ),
    (
        "warp_file",
        Nifti1,
        {
            "help_string": "filename of warpfield (e.g. intermediate2dest_warp.nii.gz)",
            "argstr": "-warp {warp_file}",
            "xor": ["xfm_file"],
        },
    ),
    (
        "coord_vox",
        bool,
        {
            "help_string": "all coordinates in voxels - default",
            "argstr": "-vox",
            "xor": ["coord_mm"],
        },
    ),
    (
        "coord_mm",
        bool,
        {"help_string": "all coordinates in mm", "argstr": "-mm", "xor": ["coord_vox"]},
    ),
]
WarpPointsFromStd_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "out_file",
        File,
        {
            "help_string": "Name of output file, containing the warp as field or coefficients."
        },
    )
]
WarpPointsFromStd_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class WarpPointsFromStd(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from fileformats.medimage.nifti import Nifti1
    >>> from fileformats.text import TextFile
    >>> from pydra.tasks.fsl.auto.warp_points_from_std import WarpPointsFromStd

    >>> task = WarpPointsFromStd()
    >>> task.inputs.img_file = Nifti1.mock("T1.nii")
    >>> task.inputs.std_file = Nifti1.mock("mni.nii")
    >>> task.inputs.in_coords = TextFile.mock("surf.txt")
    >>> task.inputs.xfm_file = File.mock()
    >>> task.inputs.warp_file = Nifti1.mock("warpfield.nii")
    >>> task.inputs.coord_mm = True
    >>> task.cmdline
    'std2imgcoord -mm -img T1.nii -std mni.nii -warp warpfield.nii surf.txt'


    """

    input_spec = WarpPointsFromStd_input_spec
    output_spec = WarpPointsFromStd_output_spec
    executable = "std2imgcoord"
