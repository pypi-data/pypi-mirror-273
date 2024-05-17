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
            "help_string": "unfiltered 4D image",
            "argstr": "-i {in_file}",
            "mandatory": True,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "output outlier file name",
            "argstr": "-o {out_file}",
            "output_file_template": "{in_file}_outliers.txt",
        },
    ),
    (
        "mask",
        File,
        {"help_string": "mask image for calculating metric", "argstr": "-m {mask}"},
    ),
    (
        "metric",
        ty.Any,
        {
            "help_string": "metrics: refrms - RMS intensity difference to reference volume as metric [default metric], refmse - Mean Square Error version of refrms (used in original version of fsl_motion_outliers), dvars - DVARS, fd - frame displacement, fdrms - FD with RMS matrix calculation",
            "argstr": "--{metric}",
        },
    ),
    (
        "threshold",
        float,
        {
            "help_string": "specify absolute threshold value (otherwise use box-plot cutoff = P75 + 1.5*IQR)",
            "argstr": "--thresh={threshold}",
        },
    ),
    (
        "no_motion_correction",
        bool,
        {
            "help_string": "do not run motion correction (assumed already done)",
            "argstr": "--nomoco",
        },
    ),
    (
        "dummy",
        int,
        {
            "help_string": "number of dummy scans to delete (before running anything and creating EVs)",
            "argstr": "--dummy={dummy}",
        },
    ),
    (
        "out_metric_values",
        Path,
        {
            "help_string": "output metric values (DVARS etc.) file name",
            "argstr": "-s {out_metric_values}",
            "output_file_template": "{in_file}_metrics.txt",
        },
    ),
    (
        "out_metric_plot",
        Path,
        {
            "help_string": "output metric values plot (DVARS etc.) file name",
            "argstr": "-p {out_metric_plot}",
            "output_file_template": "{in_file}_metrics.png",
        },
    ),
]
MotionOutliers_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
MotionOutliers_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class MotionOutliers(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from fileformats.medimage.nifti import Nifti1
    >>> from pydra.tasks.fsl.auto.motion_outliers import MotionOutliers

    >>> task = MotionOutliers()
    >>> task.inputs.in_file = Nifti1.mock("epi.nii")
    >>> task.inputs.mask = File.mock()
    >>> task.cmdline
    'fsl_motion_outliers -i epi.nii -o epi_outliers.txt -p epi_metrics.png -s epi_metrics.txt'


    """

    input_spec = MotionOutliers_input_spec
    output_spec = MotionOutliers_output_spec
    executable = "fsl_motion_outliers"
