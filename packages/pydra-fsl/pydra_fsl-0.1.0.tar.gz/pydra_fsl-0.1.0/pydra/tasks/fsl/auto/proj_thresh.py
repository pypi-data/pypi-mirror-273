from fileformats.generic.file import File
from pydra.engine import ShellCommandTask
from pydra.engine import specs
import typing as ty

input_fields = [
    (
        "in_files",
        ty.List[File],
        {
            "help_string": "a list of input volumes",
            "argstr": "{in_files}",
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "threshold",
        int,
        {
            "help_string": "threshold indicating minimum number of seed voxels entering this mask region",
            "argstr": "{threshold}",
            "mandatory": True,
            "position": 1,
        },
    ),
]
ProjThresh_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "out_files",
        ty.List[File],
        {"help_string": "path/name of output volume after thresholding"},
    )
]
ProjThresh_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ProjThresh(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from pydra.tasks.fsl.auto.proj_thresh import ProjThresh

    >>> task = ProjThresh()
    >>> task.inputs.in_files = ldir
    >>> task.inputs.threshold = 3
    >>> task.cmdline
    'proj_thresh seeds_to_M1.nii seeds_to_M2.nii 3'


    """

    input_spec = ProjThresh_input_spec
    output_spec = ProjThresh_output_spec
    executable = "proj_thresh"
