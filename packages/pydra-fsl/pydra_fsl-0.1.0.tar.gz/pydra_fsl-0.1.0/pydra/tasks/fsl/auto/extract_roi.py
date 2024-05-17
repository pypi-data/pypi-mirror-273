from fileformats.generic.file import File
from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs

input_fields = [
    (
        "in_file",
        File,
        {
            "help_string": "input file",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "roi_file",
        Path,
        {
            "help_string": "output file",
            "argstr": "{roi_file}",
            "position": 1,
            "output_file_template": '"bar.nii"',
        },
    ),
    ("x_min", int, {"help_string": "", "argstr": "{x_min}", "position": 2}),
    ("x_size", int, {"help_string": "", "argstr": "{x_size}", "position": 3}),
    ("y_min", int, {"help_string": "", "argstr": "{y_min}", "position": 4}),
    ("y_size", int, {"help_string": "", "argstr": "{y_size}", "position": 5}),
    ("z_min", int, {"help_string": "", "argstr": "{z_min}", "position": 6}),
    ("z_size", int, {"help_string": "", "argstr": "{z_size}", "position": 7}),
    ("t_min", int, {"help_string": "", "argstr": "{t_min}", "position": 8}),
    ("t_size", int, {"help_string": "", "argstr": "{t_size}", "position": 9}),
    (
        "crop_list",
        list,
        {
            "help_string": "list of two tuples specifying crop options",
            "argstr": "{crop_list}",
            "position": 2,
            "xor": [
                "x_min",
                "x_size",
                "y_min",
                "y_size",
                "z_min",
                "z_size",
                "t_min",
                "t_size",
            ],
        },
    ),
]
ExtractROI_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
ExtractROI_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ExtractROI(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from pydra.tasks.fsl.auto.extract_roi import ExtractROI

    >>> task = ExtractROI()
    >>> task.inputs.in_file = File.mock(anatfile)
    >>> task.inputs.roi_file = "bar.nii"
    >>> task.inputs.t_min = 0
    >>> task.inputs.t_size = 1
    >>> task.cmdline
    'None'


    """

    input_spec = ExtractROI_input_spec
    output_spec = ExtractROI_output_spec
    executable = "fslroi"
