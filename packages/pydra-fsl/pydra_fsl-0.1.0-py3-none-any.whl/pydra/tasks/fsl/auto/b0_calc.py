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
            "help_string": "filename of input image (usually a tissue/air segmentation)",
            "argstr": "-i {in_file}",
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "filename of B0 output volume",
            "argstr": "-o {out_file}",
            "position": 1,
            "output_file_template": "{in_file}_b0field",
        },
    ),
    (
        "x_grad",
        float,
        0.0,
        {
            "help_string": "Value for zeroth-order x-gradient field (per mm)",
            "argstr": "--gx={x_grad:0.4}",
        },
    ),
    (
        "y_grad",
        float,
        0.0,
        {
            "help_string": "Value for zeroth-order y-gradient field (per mm)",
            "argstr": "--gy={y_grad:0.4}",
        },
    ),
    (
        "z_grad",
        float,
        0.0,
        {
            "help_string": "Value for zeroth-order z-gradient field (per mm)",
            "argstr": "--gz={z_grad:0.4}",
        },
    ),
    (
        "x_b0",
        float,
        0.0,
        {
            "help_string": "Value for zeroth-order b0 field (x-component), in Tesla",
            "argstr": "--b0x={x_b0:0.2}",
            "xor": ["xyz_b0"],
        },
    ),
    (
        "y_b0",
        float,
        0.0,
        {
            "help_string": "Value for zeroth-order b0 field (y-component), in Tesla",
            "argstr": "--b0y={y_b0:0.2}",
            "xor": ["xyz_b0"],
        },
    ),
    (
        "z_b0",
        float,
        1.0,
        {
            "help_string": "Value for zeroth-order b0 field (z-component), in Tesla",
            "argstr": "--b0={z_b0:0.2}",
            "xor": ["xyz_b0"],
        },
    ),
    (
        "xyz_b0",
        ty.Any,
        {
            "help_string": "Zeroth-order B0 field in Tesla",
            "argstr": "--b0x={xyz_b0[0]:0.2} --b0y={xyz_b0[1]:0.2} --b0={xyz_b0[2]:0.2}",
            "xor": ["x_b0", "y_b0", "z_b0"],
        },
    ),
    (
        "delta",
        float,
        -9.45e-06,
        {"help_string": "Delta value (chi_tissue - chi_air)", "argstr": "-d %e"},
    ),
    (
        "chi_air",
        float,
        4e-07,
        {"help_string": "susceptibility of air", "argstr": "--chi0=%e"},
    ),
    (
        "compute_xyz",
        bool,
        False,
        {
            "help_string": "calculate and save all 3 field components (i.e. x,y,z)",
            "argstr": "--xyz",
        },
    ),
    (
        "extendboundary",
        float,
        1.0,
        {
            "help_string": "Relative proportion to extend voxels at boundary",
            "argstr": "--extendboundary={extendboundary:0.2}",
        },
    ),
    (
        "directconv",
        bool,
        False,
        {
            "help_string": "use direct (image space) convolution, not FFT",
            "argstr": "--directconv",
        },
    ),
]
B0Calc_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
B0Calc_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class B0Calc(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage.nifti import Nifti1
    >>> from pydra.tasks.fsl.auto.b0_calc import B0Calc

    >>> task = B0Calc()
    >>> task.inputs.in_file = Nifti1.mock("tissue+air_map.nii")
    >>> task.inputs.z_b0 = 3.0
    >>> task.cmdline
    'b0calc -i tissue+air_map.nii -o tissue+air_map_b0field.nii.gz --chi0=4.000000e-07 -d -9.450000e-06 --extendboundary=1.00 --b0x=0.00 --gx=0.0000 --b0y=0.00 --gy=0.0000 --b0=3.00 --gz=0.0000'


    """

    input_spec = B0Calc_input_spec
    output_spec = B0Calc_output_spec
    executable = "b0calc"
