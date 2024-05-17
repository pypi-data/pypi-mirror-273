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
            "help_string": "List all subjects' preprocessed, standard-space 4D datasets",
            "argstr": "{in_files}",
            "mandatory": True,
            "position": -1,
            "sep": " ",
        },
    ),
    (
        "group_IC_maps_4D",
        Nifti1,
        {
            "help_string": "4D image containing spatial IC maps (melodic_IC) from the whole-group ICA analysis",
            "argstr": "{group_IC_maps_4D}",
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "des_norm",
        bool,
        True,
        {
            "help_string": "Whether to variance-normalise the timecourses used as the stage-2 regressors; True is default and recommended",
            "argstr": "{des_norm}",
            "position": 2,
        },
    ),
    (
        "one_sample_group_mean",
        bool,
        {
            "help_string": "perform 1-sample group-mean test instead of generic permutation test",
            "argstr": "-1",
            "position": 3,
        },
    ),
    (
        "design_file",
        File,
        {
            "help_string": "Design matrix for final cross-subject modelling with randomise",
            "argstr": "{design_file}",
            "position": 3,
        },
    ),
    (
        "con_file",
        File,
        {
            "help_string": "Design contrasts for final cross-subject modelling with randomise",
            "argstr": "{con_file}",
            "position": 4,
        },
    ),
    (
        "n_perm",
        int,
        {
            "help_string": "Number of permutations for randomise; set to 1 for just raw tstat output, set to 0 to not run randomise at all.",
            "argstr": "{n_perm}",
            "mandatory": True,
            "position": 5,
        },
    ),
    (
        "out_dir",
        Path,
        "output",
        {
            "help_string": "This directory will be created to hold all output and logfiles",
            "argstr": "{out_dir}",
            "position": 6,
            "output_file_template": '"my_output_directory"',
        },
    ),
]
DualRegression_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
DualRegression_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class DualRegression(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from fileformats.medimage.nifti import Nifti1
    >>> from pydra.tasks.fsl.auto.dual_regression import DualRegression

    >>> task = DualRegression()
    >>> task.inputs.in_files = [Nifti1.mock("functional.nii"), Nifti1.mock("functional2.nii"), Nifti1.mock("functional3.nii")]
    >>> task.inputs.group_IC_maps_4D = Nifti1.mock("allFA.nii")
    >>> task.inputs.des_norm = False
    >>> task.inputs.one_sample_group_mean = True
    >>> task.inputs.design_file = File.mock()
    >>> task.inputs.con_file = File.mock()
    >>> task.inputs.n_perm = 10
    >>> task.inputs.out_dir = "my_output_directory"
    >>> task.cmdline
    'dual_regression allFA.nii 0 -1 10 my_output_directory functional.nii functional2.nii functional3.nii'


    """

    input_spec = DualRegression_input_spec
    output_spec = DualRegression_output_spec
    executable = "dual_regression"
