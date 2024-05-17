from fileformats.generic.file import File
from fileformats.medimage.nifti import Nifti1
from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs
import typing as ty

input_fields = [
    (
        "in_files",
        ty.List[Nifti1],
        {
            "help_string": "image, or multi-channel set of images, to be segmented",
            "argstr": "{in_files}",
            "copyfile": False,
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "out_basename",
        Path,
        {"help_string": "base name of output files", "argstr": "-o {out_basename}"},
    ),
    (
        "number_classes",
        ty.Any,
        {
            "help_string": "number of tissue-type classes",
            "argstr": "-n {number_classes}",
        },
    ),
    (
        "output_biasfield",
        bool,
        {"help_string": "output estimated bias field", "argstr": "-b"},
    ),
    (
        "output_biascorrected",
        bool,
        {"help_string": "output restored image (bias-corrected image)", "argstr": "-B"},
    ),
    (
        "img_type",
        ty.Any,
        {
            "help_string": "int specifying type of image: (1 = T1, 2 = T2, 3 = PD)",
            "argstr": "-t {img_type}",
        },
    ),
    (
        "bias_iters",
        ty.Any,
        {
            "help_string": "number of main-loop iterations during bias-field removal",
            "argstr": "-I {bias_iters}",
        },
    ),
    (
        "bias_lowpass",
        ty.Any,
        {
            "help_string": "bias field smoothing extent (FWHM) in mm",
            "argstr": "-l {bias_lowpass}",
        },
    ),
    (
        "init_seg_smooth",
        ty.Any,
        {
            "help_string": "initial segmentation spatial smoothness (during bias field estimation)",
            "argstr": "-f {init_seg_smooth:.3}",
        },
    ),
    (
        "segments",
        bool,
        {
            "help_string": "outputs a separate binary image for each tissue type",
            "argstr": "-g",
        },
    ),
    (
        "init_transform",
        File,
        {
            "help_string": "<standard2input.mat> initialise using priors",
            "argstr": "-a {init_transform}",
        },
    ),
    (
        "other_priors",
        ty.List[File],
        {"help_string": "alternative prior images", "argstr": "-A {other_priors}"},
    ),
    (
        "no_pve",
        bool,
        {
            "help_string": "turn off PVE (partial volume estimation)",
            "argstr": "--nopve",
        },
    ),
    ("no_bias", bool, {"help_string": "do not remove bias field", "argstr": "-N"}),
    ("use_priors", bool, {"help_string": "use priors throughout", "argstr": "-P"}),
    (
        "segment_iters",
        ty.Any,
        {
            "help_string": "number of segmentation-initialisation iterations",
            "argstr": "-W {segment_iters}",
        },
    ),
    (
        "mixel_smooth",
        ty.Any,
        {
            "help_string": "spatial smoothness for mixeltype",
            "argstr": "-R {mixel_smooth:.2}",
        },
    ),
    (
        "iters_afterbias",
        ty.Any,
        {
            "help_string": "number of main-loop iterations after bias-field removal",
            "argstr": "-O {iters_afterbias}",
        },
    ),
    (
        "hyper",
        ty.Any,
        {"help_string": "segmentation spatial smoothness", "argstr": "-H {hyper:.2}"},
    ),
    ("verbose", bool, {"help_string": "switch on diagnostic messages", "argstr": "-v"}),
    (
        "manual_seg",
        File,
        {"help_string": "Filename containing intensities", "argstr": "-s {manual_seg}"},
    ),
    (
        "probability_maps",
        bool,
        {"help_string": "outputs individual probability maps", "argstr": "-p"},
    ),
]
FAST_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "tissue_class_map",
        File,
        {
            "help_string": "path/name of binary segmented volume file one val for each class  _seg"
        },
    ),
    ("tissue_class_files", ty.List[File], {}),
    ("restored_image", ty.List[File], {}),
    (
        "mixeltype",
        File,
        {"help_string": "path/name of mixeltype volume file _mixeltype"},
    ),
    (
        "partial_volume_map",
        File,
        {"help_string": "path/name of partial volume file _pveseg"},
    ),
    ("partial_volume_files", ty.List[File], {}),
    ("bias_field", ty.List[File], {}),
    ("probability_maps", ty.List[File], {}),
]
FAST_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class FAST(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from fileformats.medimage.nifti import Nifti1
    >>> from pydra.tasks.fsl.auto.fast import FAST

    >>> task = FAST()
    >>> task.inputs.in_files = [Nifti1.mock("s"), Nifti1.mock("t"), Nifti1.mock("r"), Nifti1.mock("u"), Nifti1.mock("c"), Nifti1.mock("t"), Nifti1.mock("u"), Nifti1.mock("r"), Nifti1.mock("a"), Nifti1.mock("l"), Nifti1.mock("."), Nifti1.mock("n"), Nifti1.mock("i"), Nifti1.mock("i")]
    >>> task.inputs.out_basename = "fast_"
    >>> task.inputs.init_transform = File.mock()
    >>> task.inputs.manual_seg = File.mock()
    >>> task.cmdline
    'fast -o fast_ -S 1 structural.nii'


    """

    input_spec = FAST_input_spec
    output_spec = FAST_output_spec
    executable = "fast"
