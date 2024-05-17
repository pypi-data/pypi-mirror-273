from fileformats.generic.file import File
from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs

input_fields = [
    (
        "in_file",
        File,
        {
            "help_string": "input file name (4D image)",
            "argstr": "-i {in_file}",
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "output file name for the filtered data",
            "argstr": "-o {out_file}",
            "position": 2,
            "output_file_template": "out_file",
        },
    ),
    (
        "design_file",
        File,
        {
            "help_string": "name of the matrix with time courses (e.g. GLM design or MELODIC mixing matrix)",
            "argstr": "-d {design_file}",
            "mandatory": True,
            "position": 3,
        },
    ),
    (
        "filter_columns",
        list,
        {
            "help_string": "(1-based) column indices to filter out of the data",
            "argstr": "-f '{filter_columns}'",
            "mandatory": True,
            "position": 4,
            "xor": ["filter_all"],
        },
    ),
    (
        "filter_all",
        bool,
        {
            "help_string": "use all columns in the design file in denoising",
            "argstr": "-f '{filter_all}'",
            "mandatory": True,
            "position": 4,
            "xor": ["filter_columns"],
        },
    ),
    ("mask", File, {"help_string": "mask image file name", "argstr": "-m {mask}"}),
    (
        "var_norm",
        bool,
        {"help_string": "perform variance-normalization on data", "argstr": "--vn"},
    ),
    (
        "out_vnscales",
        bool,
        {
            "help_string": "output scaling factors for variance normalization",
            "argstr": "--out_vnscales",
        },
    ),
]
FilterRegressor_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
FilterRegressor_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class FilterRegressor(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.file import File
    >>> from pydra.tasks.fsl.auto.filter_regressor import FilterRegressor

    """

    input_spec = FilterRegressor_input_spec
    output_spec = FilterRegressor_output_spec
    executable = "fsl_regfilt"
