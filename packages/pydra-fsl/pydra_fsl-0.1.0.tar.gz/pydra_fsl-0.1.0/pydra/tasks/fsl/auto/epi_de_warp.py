from fileformats.generic.file import File
from fileformats.medimage.nifti import Nifti1
from pydra.engine import ShellCommandTask
from pydra.engine import specs
import typing as ty

input_fields = [
    (
        "mag_file",
        Nifti1,
        {
            "help_string": "Magnitude file",
            "argstr": "--mag {mag_file}",
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "dph_file",
        Nifti1,
        {
            "help_string": "Phase file assumed to be scaled from 0 to 4095",
            "argstr": "--dph {dph_file}",
            "mandatory": True,
        },
    ),
    (
        "exf_file",
        File,
        {
            "help_string": "example func volume (or use epi)",
            "argstr": "--exf {exf_file}",
        },
    ),
    (
        "epi_file",
        Nifti1,
        {"help_string": "EPI volume to unwarp", "argstr": "--epi {epi_file}"},
    ),
    (
        "tediff",
        float,
        2.46,
        {
            "help_string": "difference in B0 field map TEs",
            "argstr": "--tediff {tediff}",
        },
    ),
    ("esp", float, 0.58, {"help_string": "EPI echo spacing", "argstr": "--esp {esp}"}),
    (
        "sigma",
        int,
        2,
        {
            "help_string": "2D spatial gaussing smoothing                        stdev (default = 2mm)",
            "argstr": "--sigma {sigma}",
        },
    ),
    ("vsm", ty.Any, {"help_string": "voxel shift map", "argstr": "--vsm {vsm}"}),
    (
        "exfdw",
        ty.Any,
        {
            "help_string": "dewarped example func volume",
            "argstr": "--exfdw {exfdw}",
            "output_file_template": "exfdw",
        },
    ),
    (
        "epidw",
        ty.Any,
        {"help_string": "dewarped epi volume", "argstr": "--epidw {epidw}"},
    ),
    ("tmpdir", ty.Any, {"help_string": "tmpdir", "argstr": "--tmpdir {tmpdir}"}),
    ("nocleanup", bool, True, {"help_string": "no cleanup", "argstr": "--nocleanup"}),
    ("cleanup", bool, {"help_string": "cleanup", "argstr": "--cleanup"}),
]
EPIDeWarp_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("unwarped_file", File, {"help_string": "unwarped epi file"}),
    ("vsm_file", File, {"help_string": "voxel shift map"}),
    ("exf_mask", File, {"help_string": "Mask from example functional volume"}),
]
EPIDeWarp_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class EPIDeWarp(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from fileformats.medimage.nifti import Nifti1
    >>> from pydra.tasks.fsl.auto.epi_de_warp import EPIDeWarp

    >>> task = EPIDeWarp()
    >>> task.inputs.mag_file = Nifti1.mock("magnitude.nii")
    >>> task.inputs.dph_file = Nifti1.mock("phase.nii")
    >>> task.inputs.exf_file = File.mock()
    >>> task.inputs.epi_file = Nifti1.mock("functional.nii")
    >>> task.cmdline
    'epidewarp.fsl --mag magnitude.nii --dph phase.nii --epi functional.nii --esp 0.58 --exfdw .../exfdw.nii.gz --nocleanup --sigma 2 --tediff 2.46 --tmpdir .../temp --vsm .../vsm.nii.gz'


    """

    input_spec = EPIDeWarp_input_spec
    output_spec = EPIDeWarp_output_spec
    executable = "epidewarp.fsl"
