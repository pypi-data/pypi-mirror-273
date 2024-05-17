from fileformats.generic.directory import Directory
from fileformats.generic.file import File
from pathlib import Path
from pydra.engine import ShellCommandTask
from pydra.engine import specs
import typing as ty

input_fields = [
    (
        "in_file",
        File,
        {
            "help_string": "input data file",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": -3,
        },
    ),
    (
        "design_file",
        File,
        {
            "help_string": "design matrix file",
            "argstr": "{design_file}",
            "position": -2,
        },
    ),
    (
        "threshold",
        ty.Any,
        1000.0,
        {"help_string": "threshold", "argstr": "{threshold}", "position": -1},
    ),
    (
        "smooth_autocorr",
        bool,
        {"help_string": "Smooth auto corr estimates", "argstr": "-sa"},
    ),
    ("mask_size", int, {"help_string": "susan mask size", "argstr": "-ms {mask_size}"}),
    (
        "brightness_threshold",
        ty.Any,
        {
            "help_string": "susan brightness threshold, otherwise it is estimated",
            "argstr": "-epith {brightness_threshold}",
        },
    ),
    ("full_data", bool, {"help_string": "output full data", "argstr": "-v"}),
    (
        "autocorr_estimate_only",
        bool,
        {
            "help_string": "perform autocorrelation estimatation only",
            "argstr": "-ac",
            "xor": [
                "autocorr_estimate_only",
                "fit_armodel",
                "tukey_window",
                "multitaper_product",
                "use_pava",
                "autocorr_noestimate",
            ],
        },
    ),
    (
        "fit_armodel",
        bool,
        {
            "help_string": "fits autoregressive model - default is to use tukey with M=sqrt(numvols)",
            "argstr": "-ar",
            "xor": [
                "autocorr_estimate_only",
                "fit_armodel",
                "tukey_window",
                "multitaper_product",
                "use_pava",
                "autocorr_noestimate",
            ],
        },
    ),
    (
        "tukey_window",
        int,
        {
            "help_string": "tukey window size to estimate autocorr",
            "argstr": "-tukey {tukey_window}",
            "xor": [
                "autocorr_estimate_only",
                "fit_armodel",
                "tukey_window",
                "multitaper_product",
                "use_pava",
                "autocorr_noestimate",
            ],
        },
    ),
    (
        "multitaper_product",
        int,
        {
            "help_string": "multitapering with slepian tapers and num is the time-bandwidth product",
            "argstr": "-mt {multitaper_product}",
            "xor": [
                "autocorr_estimate_only",
                "fit_armodel",
                "tukey_window",
                "multitaper_product",
                "use_pava",
                "autocorr_noestimate",
            ],
        },
    ),
    (
        "use_pava",
        bool,
        {"help_string": "estimates autocorr using PAVA", "argstr": "-pava"},
    ),
    (
        "autocorr_noestimate",
        bool,
        {
            "help_string": "do not estimate autocorrs",
            "argstr": "-noest",
            "xor": [
                "autocorr_estimate_only",
                "fit_armodel",
                "tukey_window",
                "multitaper_product",
                "use_pava",
                "autocorr_noestimate",
            ],
        },
    ),
    (
        "output_pwdata",
        bool,
        {
            "help_string": "output prewhitened data and average design matrix",
            "argstr": "-output_pwdata",
        },
    ),
    (
        "results_dir",
        Path,
        "results",
        {"help_string": "directory to store results in", "argstr": "-rn {results_dir}"},
    ),
]
FILMGLS_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "param_estimates",
        ty.List[File],
        {"help_string": "Parameter estimates for each column of the design matrix"},
    ),
    (
        "residual4d",
        File,
        {"help_string": "Model fit residual mean-squared error for each time point"},
    ),
    ("dof_file", File, {"help_string": "degrees of freedom"}),
    (
        "sigmasquareds",
        File,
        {"help_string": "summary of residuals, See Woolrich, et. al., 2001"},
    ),
    (
        "results_dir",
        Directory,
        {"help_string": "directory storing model estimation output"},
    ),
    (
        "corrections",
        File,
        {"help_string": "statistical corrections used within FILM modeling"},
    ),
    ("thresholdac", File, {"help_string": "The FILM autocorrelation parameters"}),
    ("logfile", File, {"help_string": "FILM run logfile"}),
]
FILMGLS_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class FILMGLS(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic.directory import Directory
    >>> from fileformats.generic.file import File
    >>> from pydra.tasks.fsl.auto.filmgls import FILMGLS

    """

    input_spec = FILMGLS_input_spec
    output_spec = FILMGLS_output_spec
    executable = "film_gls"
