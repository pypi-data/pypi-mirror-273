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
            "help_string": "timeseries to motion-correct",
            "argstr": "-in {in_file}",
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "file to write",
            "argstr": "-out {out_file}",
            "output_file_template": '"moco.nii"',
        },
    ),
    (
        "cost",
        ty.Any,
        {"help_string": "cost function to optimize", "argstr": "-cost {cost}"},
    ),
    (
        "bins",
        int,
        {"help_string": "number of histogram bins", "argstr": "-bins {bins}"},
    ),
    (
        "dof",
        int,
        {
            "help_string": "degrees of freedom for the transformation",
            "argstr": "-dof {dof}",
        },
    ),
    (
        "ref_vol",
        int,
        {"help_string": "volume to align frames to", "argstr": "-refvol {ref_vol}"},
    ),
    (
        "scaling",
        float,
        {"help_string": "scaling factor to use", "argstr": "-scaling {scaling:.2}"},
    ),
    (
        "smooth",
        float,
        {
            "help_string": "smoothing factor for the cost function",
            "argstr": "-smooth {smooth:.2}",
        },
    ),
    (
        "rotation",
        int,
        {
            "help_string": "scaling factor for rotation tolerances",
            "argstr": "-rotation {rotation}",
        },
    ),
    (
        "stages",
        int,
        {
            "help_string": "stages (if 4, perform final search with sinc interpolation",
            "argstr": "-stages {stages}",
        },
    ),
    (
        "init",
        File,
        {"help_string": "initial transformation matrix", "argstr": "-init {init}"},
    ),
    (
        "interpolation",
        ty.Any,
        {
            "help_string": "interpolation method for transformation",
            "argstr": "-{interpolation}_final",
        },
    ),
    (
        "use_gradient",
        bool,
        {"help_string": "run search on gradient images", "argstr": "-gdt"},
    ),
    (
        "use_contour",
        bool,
        {"help_string": "run search on contour images", "argstr": "-edge"},
    ),
    (
        "mean_vol",
        bool,
        {"help_string": "register to mean volume", "argstr": "-meanvol"},
    ),
    (
        "stats_imgs",
        bool,
        {"help_string": "produce variance and std. dev. images", "argstr": "-stats"},
    ),
    (
        "save_mats",
        bool,
        {"help_string": "save transformation matrices", "argstr": "-mats"},
    ),
    (
        "save_plots",
        bool,
        {"help_string": "save transformation parameters", "argstr": "-plots"},
    ),
    (
        "save_rms",
        bool,
        {
            "help_string": "save rms displacement parameters",
            "argstr": "-rmsabs -rmsrel",
        },
    ),
    (
        "ref_file",
        File,
        {
            "help_string": "target image for motion correction",
            "argstr": "-reffile {ref_file}",
        },
    ),
]
MCFLIRT_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("variance_img", File, {"help_string": "variance image"}),
    ("std_img", File, {"help_string": "standard deviation image"}),
    ("mean_img", File, {"help_string": "mean timeseries image (if mean_vol=True)"}),
    ("par_file", File, {"help_string": "text-file with motion parameters"}),
    ("mat_file", ty.List[File], {"help_string": "transformation matrices"}),
    (
        "rms_files",
        ty.List[File],
        {"help_string": "absolute and relative displacement parameters"},
    ),
]
MCFLIRT_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class MCFLIRT(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from fileformats.medimage.nifti import Nifti1
    >>> from pydra.tasks.fsl.auto.mcflirt import MCFLIRT

    >>> task = MCFLIRT()
    >>> task.inputs.in_file = Nifti1.mock("functional.nii")
    >>> task.inputs.out_file = "moco.nii"
    >>> task.inputs.cost = "mutualinfo"
    >>> task.inputs.init = File.mock()
    >>> task.inputs.ref_file = File.mock()
    >>> task.cmdline
    'mcflirt -in functional.nii -cost mutualinfo -out moco.nii'


    """

    input_spec = MCFLIRT_input_spec
    output_spec = MCFLIRT_output_spec
    executable = "mcflirt"
