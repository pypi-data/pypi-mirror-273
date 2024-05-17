from fileformats.generic.file import File
from fileformats.medimage.diffusion import Bval
from fileformats.medimage.diffusion import Bvec
from fileformats.medimage.nifti import Nifti1
from pydra.engine import ShellCommandTask
from pydra.engine import specs

input_fields = [
    (
        "dwi",
        Nifti1,
        {
            "help_string": "diffusion weighted image data file",
            "argstr": "-k {dwi}",
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "base_name",
        str,
        "dtifit_",
        {
            "help_string": "base_name that all output files will start with",
            "argstr": "-o {base_name}",
            "position": 1,
        },
    ),
    (
        "mask",
        Nifti1,
        {
            "help_string": "bet binary mask file",
            "argstr": "-m {mask}",
            "mandatory": True,
            "position": 2,
        },
    ),
    (
        "bvecs",
        Bvec,
        {
            "help_string": "b vectors file",
            "argstr": "-r {bvecs}",
            "mandatory": True,
            "position": 3,
        },
    ),
    (
        "bvals",
        Bval,
        {
            "help_string": "b values file",
            "argstr": "-b {bvals}",
            "mandatory": True,
            "position": 4,
        },
    ),
    ("min_z", int, {"help_string": "min z", "argstr": "-z {min_z}"}),
    ("max_z", int, {"help_string": "max z", "argstr": "-Z {max_z}"}),
    ("min_y", int, {"help_string": "min y", "argstr": "-y {min_y}"}),
    ("max_y", int, {"help_string": "max y", "argstr": "-Y {max_y}"}),
    ("min_x", int, {"help_string": "min x", "argstr": "-x {min_x}"}),
    ("max_x", int, {"help_string": "max x", "argstr": "-X {max_x}"}),
    (
        "save_tensor",
        bool,
        {"help_string": "save the elements of the tensor", "argstr": "--save_tensor"},
    ),
    ("sse", bool, {"help_string": "output sum of squared errors", "argstr": "--sse"}),
    (
        "cni",
        File,
        {"help_string": "input counfound regressors", "argstr": "--cni={cni}"},
    ),
    (
        "little_bit",
        bool,
        {"help_string": "only process small area of brain", "argstr": "--littlebit"},
    ),
    (
        "gradnonlin",
        File,
        {
            "help_string": "gradient non linearities",
            "argstr": "--gradnonlin={gradnonlin}",
        },
    ),
]
DTIFit_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("V1", File, {"help_string": "path/name of file with the 1st eigenvector"}),
    ("V2", File, {"help_string": "path/name of file with the 2nd eigenvector"}),
    ("V3", File, {"help_string": "path/name of file with the 3rd eigenvector"}),
    ("L1", File, {"help_string": "path/name of file with the 1st eigenvalue"}),
    ("L2", File, {"help_string": "path/name of file with the 2nd eigenvalue"}),
    ("L3", File, {"help_string": "path/name of file with the 3rd eigenvalue"}),
    ("MD", File, {"help_string": "path/name of file with the mean diffusivity"}),
    ("FA", File, {"help_string": "path/name of file with the fractional anisotropy"}),
    ("MO", File, {"help_string": "path/name of file with the mode of anisotropy"}),
    (
        "S0",
        File,
        {
            "help_string": "path/name of file with the raw T2 signal with no diffusion weighting"
        },
    ),
    ("tensor", File, {"help_string": "path/name of file with the 4D tensor volume"}),
    ("sse", File, {"help_string": "path/name of file with the summed squared error"}),
]
DTIFit_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class DTIFit(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from fileformats.medimage.diffusion import Bval
    >>> from fileformats.medimage.diffusion import Bvec
    >>> from fileformats.medimage.nifti import Nifti1
    >>> from pydra.tasks.fsl.auto.dti_fit import DTIFit

    >>> task = DTIFit()
    >>> task.inputs.dwi = Nifti1.mock("diffusion.nii")
    >>> task.inputs.base_name = "TP"
    >>> task.inputs.mask = Nifti1.mock("mask.nii")
    >>> task.inputs.bvecs = Bvec.mock("bvecs")
    >>> task.inputs.bvals = Bval.mock("bvals")
    >>> task.inputs.cni = File.mock()
    >>> task.inputs.gradnonlin = File.mock()
    >>> task.cmdline
    'dtifit -k diffusion.nii -o TP -m mask.nii -r bvecs -b bvals'


    """

    input_spec = DTIFit_input_spec
    output_spec = DTIFit_output_spec
    executable = "dtifit"
