from fileformats.datascience.data import TextMatrix
from fileformats.generic.directory import Directory
from fileformats.generic.file import File
from fileformats.medimage.nifti import Nifti1
from fileformats.medimage.nifti import NiftiGz
from fileformats.text import TextFile
from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs
import typing as ty

input_fields = [
    (
        "feat_dir",
        Directory,
        {
            "help_string": "If a feat directory exists and temporal filtering has not been run yet, ICA_AROMA can use the files in this directory.",
            "argstr": "-feat {feat_dir}",
            "mandatory": True,
            "xor": ["in_file", "mat_file", "fnirt_warp_file", "motion_parameters"],
        },
    ),
    (
        "in_file",
        Nifti1,
        {
            "help_string": "volume to be denoised",
            "argstr": "-i {in_file}",
            "mandatory": True,
            "xor": ["feat_dir"],
        },
    ),
    (
        "out_dir",
        Path,
        {
            "help_string": "output directory",
            "argstr": "-o {out_dir}",
            "mandatory": True,
        },
    ),
    (
        "mask",
        NiftiGz,
        {
            "help_string": "path/name volume mask",
            "argstr": "-m {mask}",
            "xor": ["feat_dir"],
        },
    ),
    (
        "dim",
        int,
        {
            "help_string": "Dimensionality reduction when running MELODIC (default is automatic estimation)",
            "argstr": "-dim {dim}",
        },
    ),
    (
        "TR",
        float,
        {
            "help_string": "TR in seconds. If this is not specified the TR will be extracted from the header of the fMRI nifti file.",
            "argstr": "-tr {TR:.3}",
        },
    ),
    (
        "melodic_dir",
        Directory,
        {
            "help_string": "path to MELODIC directory if MELODIC has already been run",
            "argstr": "-meldir {melodic_dir}",
        },
    ),
    (
        "mat_file",
        TextMatrix,
        {
            "help_string": "path/name of the mat-file describing the affine registration (e.g. FSL FLIRT) of the functional data to structural space (.mat file)",
            "argstr": "-affmat {mat_file}",
            "xor": ["feat_dir"],
        },
    ),
    (
        "fnirt_warp_file",
        Nifti1,
        {
            "help_string": "File name of the warp-file describing the non-linear registration (e.g. FSL FNIRT) of the structural data to MNI152 space (.nii.gz)",
            "argstr": "-warp {fnirt_warp_file}",
            "xor": ["feat_dir"],
        },
    ),
    (
        "motion_parameters",
        TextFile,
        {
            "help_string": "motion parameters file",
            "argstr": "-mc {motion_parameters}",
            "mandatory": True,
            "xor": ["feat_dir"],
        },
    ),
    (
        "denoise_type",
        ty.Any,
        {
            "help_string": "Type of denoising strategy:\n-no: only classification, no denoising\n-nonaggr (default): non-aggresssive denoising, i.e. partial component regression\n-aggr: aggressive denoising, i.e. full component regression\n-both: both aggressive and non-aggressive denoising (two outputs)",
            "argstr": "-den {denoise_type}",
            "mandatory": True,
        },
    ),
]
ICA_AROMA_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "aggr_denoised_file",
        File,
        {"help_string": "if generated: aggressively denoised volume"},
    ),
    (
        "nonaggr_denoised_file",
        File,
        {"help_string": "if generated: non aggressively denoised volume"},
    ),
    (
        "out_dir",
        Directory,
        {
            "help_string": "directory contains (in addition to the denoised files): melodic.ica + classified_motion_components + classification_overview + feature_scores + melodic_ic_mni)"
        },
    ),
]
ICA_AROMA_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ICA_AROMA(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.datascience.data import TextMatrix
    >>> from fileformats.generic.directory import Directory
    >>> from fileformats.generic.file import File
    >>> from fileformats.medimage.nifti import Nifti1
    >>> from fileformats.medimage.nifti import NiftiGz
    >>> from fileformats.text import TextFile
    >>> from pydra.tasks.fsl.auto.ica__aroma import ICA_AROMA

    >>> task = ICA_AROMA()
    >>> task.inputs.feat_dir = Directory.mock()
    >>> task.inputs.in_file = Nifti1.mock("functional.nii")
    >>> task.inputs.out_dir = "ICA_testout"
    >>> task.inputs.mask = NiftiGz.mock("mask.nii.gz")
    >>> task.inputs.melodic_dir = Directory.mock()
    >>> task.inputs.mat_file = TextMatrix.mock("func_to_struct.mat")
    >>> task.inputs.fnirt_warp_file = Nifti1.mock("warpfield.nii")
    >>> task.inputs.motion_parameters = TextFile.mock("fsl_mcflirt_movpar.txt")
    >>> task.inputs.denoise_type = "both"
    >>> task.cmdline
    'ICA_AROMA.py -den both -warp warpfield.nii -i functional.nii -m mask.nii.gz -affmat func_to_struct.mat -mc fsl_mcflirt_movpar.txt -o .../ICA_testout'


    """

    input_spec = ICA_AROMA_input_spec
    output_spec = ICA_AROMA_output_spec
    executable = "ICA_AROMA.py"
