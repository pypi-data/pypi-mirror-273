from fileformats.generic.file import File
from fileformats.medimage.nifti import Nifti1
from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs
import typing as ty

input_fields = [
    (
        "epi",
        Nifti1,
        {
            "help_string": "EPI image",
            "argstr": "--epi={epi}",
            "mandatory": True,
            "position": -4,
        },
    ),
    (
        "t1_head",
        Nifti1,
        {
            "help_string": "wholehead T1 image",
            "argstr": "--t1={t1_head}",
            "mandatory": True,
            "position": -3,
        },
    ),
    (
        "t1_brain",
        Nifti1,
        {
            "help_string": "brain extracted T1 image",
            "argstr": "--t1brain={t1_brain}",
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "out_base",
        ty.Any,
        "epi2struct",
        {
            "help_string": "output base name",
            "argstr": "--out={out_base}",
            "position": -1,
        },
    ),
    (
        "fmap",
        Nifti1,
        {"help_string": "fieldmap image (in rad/s)", "argstr": "--fmap={fmap}"},
    ),
    (
        "fmapmag",
        Nifti1,
        {
            "help_string": "fieldmap magnitude image - wholehead",
            "argstr": "--fmapmag={fmapmag}",
        },
    ),
    (
        "fmapmagbrain",
        Nifti1,
        {
            "help_string": "fieldmap magnitude image - brain extracted",
            "argstr": "--fmapmagbrain={fmapmagbrain}",
        },
    ),
    (
        "wmseg",
        Path,
        {
            "help_string": "white matter segmentation of T1 image, has to be named                  like the t1brain and end on _wmseg",
            "argstr": "--wmseg={wmseg}",
        },
    ),
    (
        "echospacing",
        float,
        {
            "help_string": "Effective EPI echo spacing                                 (sometimes called dwell time) - in seconds",
            "argstr": "--echospacing={echospacing}",
        },
    ),
    (
        "pedir",
        ty.Any,
        {
            "help_string": "phase encoding direction, dir = x/y/z/-x/-y/-z",
            "argstr": "--pedir={pedir}",
        },
    ),
    (
        "weight_image",
        File,
        {
            "help_string": "weighting image (in T1 space)",
            "argstr": "--weight={weight_image}",
        },
    ),
    (
        "no_fmapreg",
        bool,
        {
            "help_string": "do not perform registration of fmap to T1                         (use if fmap already registered)",
            "argstr": "--nofmapreg",
        },
    ),
    (
        "no_clean",
        bool,
        True,
        {"help_string": "do not clean up intermediate files", "argstr": "--noclean"},
    ),
]
EpiReg_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("out_file", File, {"help_string": "unwarped and coregistered epi input"}),
    ("out_1vol", File, {"help_string": "unwarped and coregistered single volume"}),
    ("fmap2str_mat", File, {"help_string": "rigid fieldmap-to-structural transform"}),
    ("fmap2epi_mat", File, {"help_string": "rigid fieldmap-to-epi transform"}),
    ("fmap_epi", File, {"help_string": "fieldmap in epi space"}),
    ("fmap_str", File, {"help_string": "fieldmap in structural space"}),
    (
        "fmapmag_str",
        File,
        {"help_string": "fieldmap magnitude image in structural space"},
    ),
    ("epi2str_inv", File, {"help_string": "rigid structural-to-epi transform"}),
    ("epi2str_mat", File, {"help_string": "rigid epi-to-structural transform"}),
    ("shiftmap", File, {"help_string": "shiftmap in epi space"}),
    (
        "fullwarp",
        File,
        {
            "help_string": "warpfield to unwarp epi and transform into                     structural space"
        },
    ),
    ("wmseg", File, {"help_string": "white matter segmentation used in flirt bbr"}),
    ("seg", File, {"help_string": "white matter, gray matter, csf segmentation"}),
    ("wmedge", File, {"help_string": "white matter edges for visualization"}),
]
EpiReg_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class EpiReg(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from fileformats.medimage.nifti import Nifti1
    >>> from pydra.tasks.fsl.auto.epi_reg import EpiReg

    >>> task = EpiReg()
    >>> task.inputs.epi = Nifti1.mock("epi.nii")
    >>> task.inputs.t1_head = Nifti1.mock("T1.nii")
    >>> task.inputs.t1_brain = Nifti1.mock("T1_brain.nii")
    >>> task.inputs.out_base = "epi2struct"
    >>> task.inputs.fmap = Nifti1.mock("fieldmap_phase_fslprepared.nii")
    >>> task.inputs.fmapmag = Nifti1.mock("fieldmap_mag.nii")
    >>> task.inputs.fmapmagbrain = Nifti1.mock("fieldmap_mag_brain.nii")
    >>> task.inputs.echospacing = 0.00067
    >>> task.inputs.pedir = "y"
    >>> task.inputs.weight_image = File.mock()
    >>> task.cmdline
    'epi_reg --echospacing=0.000670 --fmap=fieldmap_phase_fslprepared.nii --fmapmag=fieldmap_mag.nii --fmapmagbrain=fieldmap_mag_brain.nii --noclean --pedir=y --epi=epi.nii --t1=T1.nii --t1brain=T1_brain.nii --out=epi2struct'


    """

    input_spec = EpiReg_input_spec
    output_spec = EpiReg_output_spec
    executable = "epi_reg"
