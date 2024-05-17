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
        {"help_string": "filename of input volume", "argstr": "--in={in_file}"},
    ),
    (
        "shift_in_file",
        Nifti1,
        {
            "help_string": "filename for reading pixel shift volume",
            "argstr": "--loadshift={shift_in_file}",
        },
    ),
    (
        "phasemap_in_file",
        Nifti1,
        {
            "help_string": "filename for input phase image",
            "argstr": "--phasemap={phasemap_in_file}",
        },
    ),
    (
        "fmap_in_file",
        File,
        {
            "help_string": "filename for loading fieldmap (rad/s)",
            "argstr": "--loadfmap={fmap_in_file}",
        },
    ),
    (
        "unwarped_file",
        Path,
        {
            "help_string": "apply unwarping and save as filename",
            "argstr": "--unwarp={unwarped_file}",
            "requires": ["in_file"],
            "xor": ["warped_file"],
        },
    ),
    (
        "warped_file",
        Path,
        {
            "help_string": "apply forward warping and save as filename",
            "argstr": "--warp={warped_file}",
            "requires": ["in_file"],
            "xor": ["unwarped_file"],
        },
    ),
    (
        "forward_warping",
        bool,
        False,
        {"help_string": "apply forward warping instead of unwarping"},
    ),
    (
        "dwell_to_asym_ratio",
        float,
        {
            "help_string": "set the dwell to asym time ratio",
            "argstr": "--dwelltoasym={dwell_to_asym_ratio:.10}",
        },
    ),
    (
        "dwell_time",
        float,
        {
            "help_string": "set the EPI dwell time per phase-encode line - same as echo spacing - (sec)",
            "argstr": "--dwell={dwell_time:.10}",
        },
    ),
    (
        "asym_se_time",
        float,
        {
            "help_string": "set the fieldmap asymmetric spin echo time (sec)",
            "argstr": "--asym={asym_se_time:.10}",
        },
    ),
    (
        "median_2dfilter",
        bool,
        {"help_string": "apply 2D median filtering", "argstr": "--median"},
    ),
    (
        "despike_2dfilter",
        bool,
        {"help_string": "apply a 2D de-spiking filter", "argstr": "--despike"},
    ),
    (
        "no_gap_fill",
        bool,
        {
            "help_string": "do not apply gap-filling measure to the fieldmap",
            "argstr": "--nofill",
        },
    ),
    (
        "no_extend",
        bool,
        {
            "help_string": "do not apply rigid-body extrapolation to the fieldmap",
            "argstr": "--noextend",
        },
    ),
    (
        "smooth2d",
        float,
        {
            "help_string": "apply 2D Gaussian smoothing of sigma N (in mm)",
            "argstr": "--smooth2={smooth2d:.2}",
        },
    ),
    (
        "smooth3d",
        float,
        {
            "help_string": "apply 3D Gaussian smoothing of sigma N (in mm)",
            "argstr": "--smooth3={smooth3d:.2}",
        },
    ),
    (
        "poly_order",
        int,
        {
            "help_string": "apply polynomial fitting of order N",
            "argstr": "--poly={poly_order}",
        },
    ),
    (
        "fourier_order",
        int,
        {
            "help_string": "apply Fourier (sinusoidal) fitting of order N",
            "argstr": "--fourier={fourier_order}",
        },
    ),
    (
        "pava",
        bool,
        {"help_string": "apply monotonic enforcement via PAVA", "argstr": "--pava"},
    ),
    (
        "despike_threshold",
        float,
        {
            "help_string": "specify the threshold for de-spiking (default=3.0)",
            "argstr": "--despikethreshold={despike_threshold}",
        },
    ),
    (
        "unwarp_direction",
        ty.Any,
        {
            "help_string": "specifies direction of warping (default y)",
            "argstr": "--unwarpdir={unwarp_direction}",
        },
    ),
    (
        "phase_conjugate",
        bool,
        {
            "help_string": "apply phase conjugate method of unwarping",
            "argstr": "--phaseconj",
        },
    ),
    (
        "icorr",
        bool,
        {
            "help_string": "apply intensity correction to unwarping (pixel shift method only)",
            "argstr": "--icorr",
            "requires": ["shift_in_file"],
        },
    ),
    (
        "icorr_only",
        bool,
        {
            "help_string": "apply intensity correction only",
            "argstr": "--icorronly",
            "requires": ["unwarped_file"],
        },
    ),
    (
        "mask_file",
        Nifti1,
        {
            "help_string": "filename for loading valid mask",
            "argstr": "--mask={mask_file}",
        },
    ),
    (
        "nokspace",
        bool,
        {"help_string": "do not use k-space forward warping", "argstr": "--nokspace"},
    ),
    (
        "save_shift",
        bool,
        {"help_string": "write pixel shift volume", "xor": ["save_unmasked_shift"]},
    ),
    (
        "shift_out_file",
        Path,
        {
            "help_string": "filename for saving pixel shift volume",
            "argstr": "--saveshift={shift_out_file}",
        },
    ),
    (
        "save_unmasked_shift",
        bool,
        {
            "help_string": "saves the unmasked shiftmap when using --saveshift",
            "argstr": "--unmaskshift",
            "xor": ["save_shift"],
        },
    ),
    (
        "save_fmap",
        bool,
        {"help_string": "write field map volume", "xor": ["save_unmasked_fmap"]},
    ),
    (
        "fmap_out_file",
        Path,
        {
            "help_string": "filename for saving fieldmap (rad/s)",
            "argstr": "--savefmap={fmap_out_file}",
        },
    ),
    (
        "save_unmasked_fmap",
        bool,
        {
            "help_string": "saves the unmasked fieldmap when using --savefmap",
            "argstr": "--unmaskfmap",
            "xor": ["save_fmap"],
        },
    ),
]
FUGUE_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("unwarped_file", File, {"help_string": "unwarped file"}),
    ("warped_file", File, {"help_string": "forward warped file"}),
    ("shift_out_file", File, {"help_string": "voxel shift map file"}),
    ("fmap_out_file", File, {"help_string": "fieldmap file"}),
]
FUGUE_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class FUGUE(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from fileformats.medimage.nifti import Nifti1
    >>> from pydra.tasks.fsl.auto.fugue import FUGUE

    >>> task = FUGUE()
    >>> task.inputs.in_file = Nifti1.mock("epi.nii")
    >>> task.inputs.shift_in_file = Nifti1.mock("vsm.nii"  # Previously computed with fugue as well)
    >>> task.inputs.phasemap_in_file = Nifti1.mock()
    >>> task.inputs.fmap_in_file = File.mock()
    >>> task.inputs.unwarp_direction = "y"
    >>> task.inputs.mask_file = Nifti1.mock("epi_mask.nii")
    >>> task.cmdline
    'fugue --in=epi.nii --mask=epi_mask.nii --loadshift=vsm.nii --unwarpdir=y --unwarp=epi_unwarped.nii.gz'


    >>> task = FUGUE()
    >>> task.inputs.in_file = Nifti1.mock("epi.nii")
    >>> task.inputs.shift_in_file = Nifti1.mock("vsm.nii"  # Previously computed with fugue as well)
    >>> task.inputs.phasemap_in_file = Nifti1.mock()
    >>> task.inputs.fmap_in_file = File.mock()
    >>> task.inputs.forward_warping = True
    >>> task.inputs.unwarp_direction = "y"
    >>> task.inputs.mask_file = Nifti1.mock("epi_mask.nii")
    >>> task.cmdline
    'fugue --in=epi.nii --mask=epi_mask.nii --loadshift=vsm.nii --unwarpdir=y --warp=epi_warped.nii.gz'


    >>> task = FUGUE()
    >>> task.inputs.in_file = Nifti1.mock()
    >>> task.inputs.shift_in_file = Nifti1.mock()
    >>> task.inputs.phasemap_in_file = Nifti1.mock("epi_phasediff.nii")
    >>> task.inputs.fmap_in_file = File.mock()
    >>> task.inputs.dwell_to_asym_ratio = (0.77e-3 * 3) / 2.46e-3
    >>> task.inputs.unwarp_direction = "y"
    >>> task.inputs.mask_file = Nifti1.mock("epi_mask.nii")
    >>> task.inputs.save_shift = True
    >>> task.cmdline
    'fugue --dwelltoasym=0.9390243902 --mask=epi_mask.nii --phasemap=epi_phasediff.nii --saveshift=epi_phasediff_vsm.nii.gz --unwarpdir=y'


    """

    input_spec = FUGUE_input_spec
    output_spec = FUGUE_output_spec
    executable = "fugue"
