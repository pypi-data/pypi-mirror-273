from fileformats.generic.file import File
from pydra.engine import ShellCommandTask
from pydra.engine import specs

input_fields = [
    (
        "spatial_data_file",
        File,
        {
            "help_string": "statistics spatial map",
            "argstr": '--sdf="{spatial_data_file}"',
            "copyfile": False,
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "mask",
        File,
        {
            "help_string": "mask file",
            "argstr": '--mask="{mask}"',
            "copyfile": False,
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "no_deactivation_class",
        bool,
        {
            "help_string": "enforces no deactivation class",
            "argstr": "--zfstatmode",
            "position": 2,
        },
    ),
]
SMM_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("null_p_map", File, {}),
    ("activation_p_map", File, {}),
    ("deactivation_p_map", File, {}),
]
SMM_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class SMM(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from pydra.tasks.fsl.auto.smm import SMM

    """

    input_spec = SMM_input_spec
    output_spec = SMM_output_spec
    executable = "mm --ld=logdir"
