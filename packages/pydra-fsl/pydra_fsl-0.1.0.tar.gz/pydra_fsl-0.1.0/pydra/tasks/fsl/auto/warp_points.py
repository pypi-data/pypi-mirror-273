from fileformats.generic.file import File
from fileformats.medimage.nifti import Nifti1
from fileformats.text import TextFile
from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs

input_fields = [
    (
        "src_file",
        Nifti1,
        {
            "help_string": "filename of source image",
            "argstr": "-src {src_file}",
            "mandatory": True,
        },
    ),
    (
        "dest_file",
        Nifti1,
        {
            "help_string": "filename of destination image",
            "argstr": "-dest {dest_file}",
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
            "position": -1,
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
    (
        "out_file",
        Path,
        {
            "help_string": "output file name",
            "output_file_template": "{in_coords}_warped",
        },
    ),
]
WarpPoints_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
WarpPoints_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class WarpPoints(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from fileformats.medimage.nifti import Nifti1
    >>> from fileformats.text import TextFile
    >>> from pydra.tasks.fsl.auto.warp_points import WarpPoints

    >>> task = WarpPoints()
    >>> task.inputs.src_file = Nifti1.mock("epi.nii")
    >>> task.inputs.dest_file = Nifti1.mock("T1.nii")
    >>> task.inputs.in_coords = TextFile.mock("surf.txt")
    >>> task.inputs.xfm_file = File.mock()
    >>> task.inputs.warp_file = Nifti1.mock("warpfield.nii")
    >>> task.inputs.coord_mm = True
    >>> task.cmdline
    'img2imgcoord -mm -dest T1.nii -src epi.nii -warp warpfield.nii surf.txt'


    """

    input_spec = WarpPoints_input_spec
    output_spec = WarpPoints_output_spec
    executable = "img2imgcoord"
