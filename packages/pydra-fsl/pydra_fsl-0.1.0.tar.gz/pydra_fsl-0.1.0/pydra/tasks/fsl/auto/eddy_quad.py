from fileformats.generic.file import File
from fileformats.medimage.diffusion import Bval
from fileformats.medimage.diffusion import Bvec
from fileformats.text import TextFile
from pydra.engine import ShellCommandTask
from pydra.engine import specs
import typing as ty

input_fields = [
    (
        "base_name",
        str,
        "eddy_corrected",
        {
            "help_string": "Basename (including path) for EDDY output files, i.e., corrected images and QC files",
            "argstr": "{base_name}",
            "position": 0,
        },
    ),
    (
        "idx_file",
        File,
        {
            "help_string": "File containing indices for all volumes into acquisition parameters",
            "argstr": "--eddyIdx {idx_file}",
            "mandatory": True,
        },
    ),
    (
        "param_file",
        TextFile,
        {
            "help_string": "File containing acquisition parameters",
            "argstr": "--eddyParams {param_file}",
            "mandatory": True,
        },
    ),
    (
        "mask_file",
        File,
        {
            "help_string": "Binary mask file",
            "argstr": "--mask {mask_file}",
            "mandatory": True,
        },
    ),
    (
        "bval_file",
        Bval,
        {
            "help_string": "b-values file",
            "argstr": "--bvals {bval_file}",
            "mandatory": True,
        },
    ),
    (
        "bvec_file",
        Bvec,
        {
            "help_string": "b-vectors file - only used when <base_name>.eddy_residuals file is present",
            "argstr": "--bvecs {bvec_file}",
        },
    ),
    (
        "output_dir",
        str,
        {
            "help_string": "Output directory - default = '<base_name>.qc'",
            "argstr": "--output-dir {output_dir}",
        },
    ),
    (
        "field",
        File,
        {"help_string": "TOPUP estimated field (in Hz)", "argstr": "--field {field}"},
    ),
    (
        "slice_spec",
        File,
        {
            "help_string": "Text file specifying slice/group acquisition",
            "argstr": "--slspec {slice_spec}",
        },
    ),
    ("verbose", bool, {"help_string": "Display debug messages", "argstr": "--verbose"}),
]
EddyQuad_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "qc_json",
        File,
        {
            "help_string": "Single subject database containing quality metrics and data info."
        },
    ),
    ("qc_pdf", File, {"help_string": "Single subject QC report."}),
    (
        "avg_b_png",
        ty.List[File],
        {
            "help_string": "Image showing mid-sagittal, -coronal and -axial slices of each averaged b-shell volume."
        },
    ),
    (
        "avg_b0_pe_png",
        ty.List[File],
        {
            "help_string": "Image showing mid-sagittal, -coronal and -axial slices of each averaged pe-direction b0 volume. Generated when using the -f option."
        },
    ),
    (
        "cnr_png",
        ty.List[File],
        {
            "help_string": "Image showing mid-sagittal, -coronal and -axial slices of each b-shell CNR volume. Generated when CNR maps are available."
        },
    ),
    (
        "vdm_png",
        File,
        {
            "help_string": "Image showing mid-sagittal, -coronal and -axial slices of the voxel displacement map. Generated when using the -f option."
        },
    ),
    (
        "residuals",
        File,
        {
            "help_string": "Text file containing the volume-wise mask-averaged squared residuals. Generated when residual maps are available."
        },
    ),
    (
        "clean_volumes",
        File,
        {
            "help_string": "Text file containing a list of clean volumes, based on the eddy squared residuals. To generate a version of the pre-processed dataset without outlier volumes, use: `fslselectvols -i <eddy_corrected_data> -o eddy_corrected_data_clean --vols=vols_no_outliers.txt`"
        },
    ),
]
EddyQuad_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class EddyQuad(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from fileformats.medimage.diffusion import Bval
    >>> from fileformats.medimage.diffusion import Bvec
    >>> from fileformats.text import TextFile
    >>> from pydra.tasks.fsl.auto.eddy_quad import EddyQuad

    >>> task = EddyQuad()
    >>> task.inputs.idx_file = File.mock()
    >>> task.inputs.param_file = TextFile.mock("epi_acqp.txt")
    >>> task.inputs.mask_file = File.mock()
    >>> task.inputs.bval_file = Bval.mock()
    >>> task.inputs.bvec_file = Bvec.mock()
    >>> task.inputs.output_dir = "eddy_corrected.qc"
    >>> task.inputs.field = File.mock()
    >>> task.inputs.slice_spec = File.mock()
    >>> task.cmdline
    'eddy_quad eddy_corrected --bvals bvals.scheme --bvecs bvecs.scheme --field fieldmap_phase_fslprepared.nii --eddyIdx epi_index.txt --mask epi_mask.nii --output-dir eddy_corrected.qc --eddyParams epi_acqp.txt --verbose'


    """

    input_spec = EddyQuad_input_spec
    output_spec = EddyQuad_output_spec
    executable = "eddy_quad"
