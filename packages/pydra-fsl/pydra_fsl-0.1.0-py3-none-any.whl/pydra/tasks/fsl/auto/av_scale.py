from fileformats.generic.file import File
from pydra.engine import ShellCommandTask
from pydra.engine import specs


def average_scaling_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["average_scaling"]


def determinant_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["determinant"]


def left_right_orientation_preserved_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["left_right_orientation_preserved"]


input_fields = [
    ("all_param", bool, {"help_string": "", "argstr": "--allparams"}),
    (
        "mat_file",
        File,
        {"help_string": "mat file to read", "argstr": "{mat_file}", "position": -2},
    ),
    (
        "ref_file",
        File,
        {
            "help_string": "reference file to get center of rotation",
            "argstr": "{ref_file}",
            "position": -1,
        },
    ),
]
AvScale_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "rotation_translation_matrix",
        list,
        {"help_string": "Rotation and Translation Matrix"},
    ),
    ("scales", list, {"help_string": "Scales (x,y,z)"}),
    ("skews", list, {"help_string": "Skews"}),
    (
        "average_scaling",
        float,
        {"help_string": "Average Scaling", "callable": "average_scaling_callable"},
    ),
    (
        "determinant",
        float,
        {"help_string": "Determinant", "callable": "determinant_callable"},
    ),
    ("forward_half_transform", list, {"help_string": "Forward Half Transform"}),
    ("backward_half_transform", list, {"help_string": "Backwards Half Transform"}),
    (
        "left_right_orientation_preserved",
        bool,
        {
            "help_string": "True if LR orientation preserved",
            "callable": "left_right_orientation_preserved_callable",
        },
    ),
    ("rot_angles", list, {"help_string": "rotation angles"}),
    ("translations", list, {"help_string": "translations"}),
]
AvScale_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class AvScale(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from pydra.tasks.fsl.auto.av_scale import AvScale

    """

    input_spec = AvScale_input_spec
    output_spec = AvScale_output_spec
    executable = "avscale"
