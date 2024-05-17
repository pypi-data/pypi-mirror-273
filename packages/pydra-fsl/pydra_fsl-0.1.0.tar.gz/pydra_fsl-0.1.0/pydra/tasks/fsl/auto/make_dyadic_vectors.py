from fileformats.generic.file import File
from pydra.engine import ShellCommandTask
from pydra.engine import specs

input_fields = [
    (
        "theta_vol",
        File,
        {"help_string": "", "argstr": "{theta_vol}", "mandatory": True, "position": 0},
    ),
    (
        "phi_vol",
        File,
        {"help_string": "", "argstr": "{phi_vol}", "mandatory": True, "position": 1},
    ),
    ("mask", File, {"help_string": "", "argstr": "{mask}", "position": 2}),
    ("output", File, "dyads", {"help_string": "", "argstr": "{output}", "position": 3}),
    (
        "perc",
        float,
        {
            "help_string": "the {perc}% angle of the output cone of uncertainty (output will be in degrees)",
            "argstr": "{perc}",
            "position": 4,
        },
    ),
]
MakeDyadicVectors_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("dyads", File, {}), ("dispersion", File, {})]
MakeDyadicVectors_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class MakeDyadicVectors(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from pydra.tasks.fsl.auto.make_dyadic_vectors import MakeDyadicVectors

    """

    input_spec = MakeDyadicVectors_input_spec
    output_spec = MakeDyadicVectors_output_spec
    executable = "make_dyadic_vectors"
