from fileformats.datascience.data import TextMatrix
from fileformats.generic.file import File
from fileformats.medimage.nifti import Nifti1
from fileformats.medimage_fsl import Con
from pydra.engine import ShellCommandTask
from pydra.engine import specs
import typing as ty

input_fields = [
    (
        "in_file",
        Nifti1,
        {
            "help_string": "4D input file",
            "argstr": "-i {in_file}",
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "base_name",
        str,
        "randomise",
        {
            "help_string": "the rootname that all generated files will have",
            "argstr": '-o "{base_name}"',
            "position": 1,
        },
    ),
    (
        "design_mat",
        TextMatrix,
        {
            "help_string": "design matrix file",
            "argstr": "-d {design_mat}",
            "position": 2,
        },
    ),
    (
        "tcon",
        Con,
        {"help_string": "t contrasts file", "argstr": "-t {tcon}", "position": 3},
    ),
    ("fcon", File, {"help_string": "f contrasts file", "argstr": "-f {fcon}"}),
    ("mask", Nifti1, {"help_string": "mask image", "argstr": "-m {mask}"}),
    (
        "x_block_labels",
        File,
        {
            "help_string": "exchangeability block labels file",
            "argstr": "-e {x_block_labels}",
        },
    ),
    (
        "demean",
        bool,
        {"help_string": "demean data temporally before model fitting", "argstr": "-D"},
    ),
    (
        "one_sample_group_mean",
        bool,
        {
            "help_string": "perform 1-sample group-mean test instead of generic permutation test",
            "argstr": "-1",
        },
    ),
    (
        "show_total_perms",
        bool,
        {
            "help_string": "print out how many unique permutations would be generated and exit",
            "argstr": "-q",
        },
    ),
    (
        "show_info_parallel_mode",
        bool,
        {
            "help_string": "print out information required for parallel mode and exit",
            "argstr": "-Q",
        },
    ),
    (
        "vox_p_values",
        bool,
        {
            "help_string": "output voxelwise (corrected and uncorrected) p-value images",
            "argstr": "-x",
        },
    ),
    (
        "tfce",
        bool,
        {"help_string": "carry out Threshold-Free Cluster Enhancement", "argstr": "-T"},
    ),
    (
        "tfce2D",
        bool,
        {
            "help_string": "carry out Threshold-Free Cluster Enhancement with 2D optimisation",
            "argstr": "--T2",
        },
    ),
    (
        "f_only",
        bool,
        {"help_string": "calculate f-statistics only", "argstr": "--fonly"},
    ),
    (
        "raw_stats_imgs",
        bool,
        {"help_string": "output raw ( unpermuted ) statistic images", "argstr": "-R"},
    ),
    (
        "p_vec_n_dist_files",
        bool,
        {
            "help_string": "output permutation vector and null distribution text files",
            "argstr": "-P",
        },
    ),
    (
        "num_perm",
        int,
        {
            "help_string": "number of permutations (default 5000, set to 0 for exhaustive)",
            "argstr": "-n {num_perm}",
        },
    ),
    (
        "seed",
        int,
        {
            "help_string": "specific integer seed for random number generator",
            "argstr": "--seed={seed}",
        },
    ),
    (
        "var_smooth",
        int,
        {
            "help_string": "use variance smoothing (std is in mm)",
            "argstr": "-v {var_smooth}",
        },
    ),
    (
        "c_thresh",
        float,
        {
            "help_string": "carry out cluster-based thresholding",
            "argstr": "-c {c_thresh:.1}",
        },
    ),
    (
        "cm_thresh",
        float,
        {
            "help_string": "carry out cluster-mass-based thresholding",
            "argstr": "-C {cm_thresh:.1}",
        },
    ),
    (
        "f_c_thresh",
        float,
        {
            "help_string": "carry out f cluster thresholding",
            "argstr": "-F {f_c_thresh:.2}",
        },
    ),
    (
        "f_cm_thresh",
        float,
        {
            "help_string": "carry out f cluster-mass thresholding",
            "argstr": "-S {f_cm_thresh:.2}",
        },
    ),
    (
        "tfce_H",
        float,
        {
            "help_string": "TFCE height parameter (default=2)",
            "argstr": "--tfce_H={tfce_H:.2}",
        },
    ),
    (
        "tfce_E",
        float,
        {
            "help_string": "TFCE extent parameter (default=0.5)",
            "argstr": "--tfce_E={tfce_E:.2}",
        },
    ),
    (
        "tfce_C",
        float,
        {
            "help_string": "TFCE connectivity (6 or 26; default=6)",
            "argstr": "--tfce_C={tfce_C:.2}",
        },
    ),
]
Randomise_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("tstat_files", ty.List[File], {"help_string": "t contrast raw statistic"}),
    ("fstat_files", ty.List[File], {"help_string": "f contrast raw statistic"}),
    (
        "t_p_files",
        ty.List[File],
        {"help_string": "f contrast uncorrected p values files"},
    ),
    (
        "f_p_files",
        ty.List[File],
        {"help_string": "f contrast uncorrected p values files"},
    ),
    (
        "t_corrected_p_files",
        ty.List[File],
        {"help_string": "t contrast FWE (Family-wise error) corrected p values files"},
    ),
    (
        "f_corrected_p_files",
        ty.List[File],
        {"help_string": "f contrast FWE (Family-wise error) corrected p values files"},
    ),
]
Randomise_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Randomise(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.datascience.data import TextMatrix
    >>> from fileformats.generic.file import File
    >>> from fileformats.medimage.nifti import Nifti1
    >>> from fileformats.medimage_fsl import Con
    >>> from pydra.tasks.fsl.auto.randomise import Randomise

    >>> task = Randomise()
    >>> task.inputs.in_file = Nifti1.mock("allFA.nii")
    >>> task.inputs.design_mat = TextMatrix.mock("design.mat")
    >>> task.inputs.tcon = Con.mock("design.con")
    >>> task.inputs.fcon = File.mock()
    >>> task.inputs.mask = Nifti1.mock("mask.nii")
    >>> task.inputs.x_block_labels = File.mock()
    >>> task.cmdline
    'randomise -i allFA.nii -o "randomise" -d design.mat -t design.con -m mask.nii'


    """

    input_spec = Randomise_input_spec
    output_spec = Randomise_output_spec
    executable = "randomise"
