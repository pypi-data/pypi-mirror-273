from fileformats.generic.file import File
from pydra.engine import ShellCommandTask
from pydra.engine import specs
import typing as ty

input_fields = [
    (
        "tcon_file",
        File,
        {
            "help_string": "contrast file containing T-contrasts",
            "argstr": "{tcon_file}",
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "fcon_file",
        File,
        {
            "help_string": "contrast file containing F-contrasts",
            "argstr": "-f {fcon_file}",
        },
    ),
    (
        "param_estimates",
        ty.List[File],
        {
            "help_string": "Parameter estimates for each column of the design matrix",
            "argstr": "",
            "copyfile": False,
            "mandatory": True,
        },
    ),
    (
        "corrections",
        File,
        {
            "help_string": "statistical corrections used within FILM modelling",
            "copyfile": False,
            "mandatory": True,
        },
    ),
    (
        "dof_file",
        File,
        {
            "help_string": "degrees of freedom",
            "argstr": "",
            "copyfile": False,
            "mandatory": True,
        },
    ),
    (
        "sigmasquareds",
        File,
        {
            "help_string": "summary of residuals, See Woolrich, et. al., 2001",
            "argstr": "",
            "copyfile": False,
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "contrast_num",
        ty.Any,
        {
            "help_string": "contrast number to start labeling copes from",
            "argstr": "-cope",
        },
    ),
    (
        "suffix",
        str,
        {
            "help_string": "suffix to put on the end of the cope filename before the contrast number, default is nothing",
            "argstr": "-suffix {suffix}",
        },
    ),
]
ContrastMgr_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("copes", ty.List[File], {"help_string": "Contrast estimates for each contrast"}),
    (
        "varcopes",
        ty.List[File],
        {"help_string": "Variance estimates for each contrast"},
    ),
    ("zstats", ty.List[File], {"help_string": "z-stat file for each contrast"}),
    ("tstats", ty.List[File], {"help_string": "t-stat file for each contrast"}),
    ("fstats", ty.List[File], {"help_string": "f-stat file for each contrast"}),
    ("zfstats", ty.List[File], {"help_string": "z-stat file for each F contrast"}),
    ("neffs", ty.List[File], {"help_string": "neff file ?? for each contrast"}),
]
ContrastMgr_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ContrastMgr(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from pydra.tasks.fsl.auto.contrast_mgr import ContrastMgr

    """

    input_spec = ContrastMgr_input_spec
    output_spec = ContrastMgr_output_spec
    executable = "contrast_mgr"
