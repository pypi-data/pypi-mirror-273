from fileformats.datascience.data import TextMatrix
from fileformats.generic.file import File
from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs

input_fields = [
    (
        "in_file",
        TextMatrix,
        {
            "help_string": "input transformation matrix",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "in_file2",
        File,
        {
            "help_string": "second input matrix (for use with fix_scale_skew or concat_xfm)",
            "argstr": "{in_file2}",
            "position": -2,
        },
    ),
    (
        "invert_xfm",
        bool,
        {
            "help_string": "invert input transformation",
            "argstr": "-inverse",
            "position": -3,
            "xor": ["invert_xfm", "concat_xfm", "fix_scale_skew"],
        },
    ),
    (
        "concat_xfm",
        bool,
        {
            "help_string": "write joint transformation of two input matrices",
            "argstr": "-concat",
            "position": -3,
            "requires": ["in_file2"],
            "xor": ["invert_xfm", "concat_xfm", "fix_scale_skew"],
        },
    ),
    (
        "fix_scale_skew",
        bool,
        {
            "help_string": "use secondary matrix to fix scale and skew",
            "argstr": "-fixscaleskew",
            "position": -3,
            "requires": ["in_file2"],
            "xor": ["invert_xfm", "concat_xfm", "fix_scale_skew"],
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "final transformation matrix",
            "argstr": "-omat {out_file}",
            "position": 1,
            "output_file_template": '"flirt_inv.mat"',
        },
    ),
]
ConvertXFM_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
ConvertXFM_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ConvertXFM(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.datascience.data import TextMatrix
    >>> from fileformats.generic.file import File
    >>> from pydra.tasks.fsl.auto.convert_xfm import ConvertXFM

    >>> task = ConvertXFM()
    >>> task.inputs.in_file = TextMatrix.mock("flirt.mat")
    >>> task.inputs.in_file2 = File.mock()
    >>> task.inputs.invert_xfm = True
    >>> task.inputs.out_file = "flirt_inv.mat"
    >>> task.cmdline
    'convert_xfm -omat flirt_inv.mat -inverse flirt.mat'


    """

    input_spec = ConvertXFM_input_spec
    output_spec = ConvertXFM_output_spec
    executable = "convert_xfm"
