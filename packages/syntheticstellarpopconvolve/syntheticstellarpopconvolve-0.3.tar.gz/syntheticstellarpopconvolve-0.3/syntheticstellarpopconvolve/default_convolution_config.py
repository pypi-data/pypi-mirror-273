"""
File containing the default values and the validations for the configuration of the convolution

TODO: always require the starformation array function to accept config and time_centers
TODO: always require the metallicity array function to accept config, time_centers, metallicity centers
TODO: allow a better configuration for the starformation rate, instead of having the time-bins decide how that starformation rate array is resolved
TODO: allow passing a unit for the starformation rate
"""

import copy
import logging
import os
from typing import Callable

import astropy.units as u
import numpy as np
import voluptuous as vol
from astropy.cosmology import Planck13 as cosmo  # Planck 2013

ALLOWED_NUMERICAL_TYPES = (int, float, complex, np.number)
dimensionless_unit = u.m / u.m

##########
# Logger configuration
logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s ] %(asctime)s: %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.INFO)


#################
# Validation routines
def unit_validation(value):
    # allow 'astropy.units.core.Unit, 'astropy.units.quantity.Quantity', 'astropy.units.core.CompositeUnit'
    if not isinstance(value, (type(u.yr), type(1 / u.Msun), type(u.Msun**-1))):
        raise ValueError("Input has to be a astropy-unit object")


def logger_validation(value):
    if not isinstance(value, type(logger)):
        raise ValueError("Input has to be a logging-type object")


def callable_validation(value):
    if not isinstance(value, Callable):
        raise ValueError("Input has to be a callable")


def callable_or_none_validation(value):
    if value is not None:
        if not isinstance(value, Callable):
            raise ValueError("Input has to be a callable")


def array_validation(value):
    if not isinstance(value, type(np.array([]))):
        raise ValueError("Input has to be a numpy array")


def existing_path_validation(value):
    if isinstance(value, str):
        if not os.path.isfile(value):
            raise ValueError("File doesnt exist")
    else:
        raise ValueError("Please provide a string-based input")


#
boolean_int_validation = vol.All(vol.Range(max=1), vol.Boolean())
float_or_int = vol.Or(float, int)

############################
#
default_convolution_config_dict = {
    ###################
    # Convolution configuration
    "time_type": {
        "value": "redshift",
        "description": "Time-type used in convolution. Can be either 'redshift' or 'lookback_time'",
        "validation": vol.All(
            str,
            vol.In(["redshift", "lookback_time"]),
        ),
    },
    # ###################
    # # Starformation related
    "SFR_info": {
        "value": {},
        "description": "dictionary containing the starformation rate info. Can also be a list of dictionaries.",
    },
    # # Global starformation rate config
    # "star_formation_rate_distribution_function": {
    #     "value": madau_dickinson_sfr,
    #     "description": "Function to calculate the star formation rate (density) with. This function needs to accept either time or redshift, and the parameters that are passed with 'star_formation_rate_distribution_args'. This function needs to return an astropy unit object of either 'mass per time per volume' or a 'mass per time'.",
    #     "validation": callable_validation,  # TODO: improve validation
    # },
    # "star_formation_rate_distribution_args": {
    #     "value": {
    #         # Star formation rate for madau dickinson-type SFR with the configurations of van Son 2021
    #         "a": 0.02,
    #         "b": 1.48,
    #         "c": 4.45,
    #         "d": 5.90,
    #     },
    #     "description": "Arguments for the star formation rate (density) function. See 'star_formation_rate_function'.",
    #     "validation": dict,
    # },
    # "star_formation_rate_distribution_time_bin_edges": {
    #     "value": np.arange(0, 10, 0.025),
    #     "description": "time-quantity array (lookback-time or redshift) on which the star formation rates are calculated.",
    #     "validation": array_validation,
    # },
    # # TODO: change the setup s.t. user can just provide a function that sets the values
    # # "star_formation_distribution_use_file": {
    # #     "value": False,
    # #     "description": "Whether to use a starformation rate file that contains the data.",  # TODO: expand explanation
    # #     "validation": boolean_int_validation,
    # # },
    # # "star_formation_distribution_filename": {
    # #     "value": "",
    # #     "description": "Filename of the SFR file.",  # TODO: expand explanation. likely cahnge t
    # #     "validation": existing_path_validation,
    # # },
    # # Global metallicity distribution config
    # "metallicity_distribution_function": {
    #     "value": compas_metallicity_distribution,
    #     "description": "Function to calculate the metallicity distribution with. This function needs to accept either time or redshift, and the parameters that are passed with 'metallicity_distribution_args'. ",
    #     "validation": callable_validation,  # TODO: improve validation
    # },
    # "metallicity_distribution_args": {
    #     "value": {
    #         # # metallicity distribution settings for Neijssel 2019
    #         # 'mu0': 0.035,
    #         # 'muz': -0.23,
    #         # 'sigma_0': 0.39,
    #         # 'sigma_z': 0.0
    #         # 'alpha': 0.0,
    #         # metallicity distribution settings for van Son 2021
    #         "mu0": 0.025,
    #         "muz": -0.05,
    #         "sigma_0": 1.125,
    #         "sigma_z": 0.05,
    #         "alpha": -1.77,
    #     },
    #     "description": "Arguments for the star formation rate (density) function. See 'metallicity_distribution_function'.",
    #     "validation": dict,
    # },
    # "metallicity_distribution_min_value": {
    #     "value": 1e-8,
    #     "description": "Minimum value to calculate the global metallicity distribution at.",
    #     "validation": float,
    # },
    # "metallicity_distribution_max_value": {
    #     "value": 1.0,
    #     "description": "Maximum value to calculate the global metallicity distribution at.",
    #     "validation": float,
    # },
    # "metallicity_distribution_resolution": {
    #     "value": 10000,
    #     "description": "Resolution to calculate the global metallicity distibution in.",
    #     "validation": int,
    # },
    # Convolution time bins
    "convolution_lookback_time_bin_edges": {
        "value": None,
        "description": "Lookback-time bin-edges used in convolution.",  # TODO: update this if we do things with units
        "validation": array_validation,
    },
    "convolution_redshift_bin_edges": {
        "value": None,
        "description": "Redshift bin-edges used in convolution.",  # TODO: update this if we do things with units
        "validation": array_validation,
    },
    # # Convolution metallicity bins
    # "convolution_metallicity_bin_edges": {
    #     "value": 10 ** np.linspace(-5, 0.5, 8),
    #     "description": "Metallicity bin-edges used in convolution.",  # TODO: expand explanation. Also consider if this is the best way
    #     "validation": array_validation,
    # },
    ###################
    # Redshift interpolator settings
    "redshift_interpolator_force_rebuild": {
        "value": False,
        "description": "Whether to force rebuild the redshift interpolator.",  # TODO: expand explanation
        "validation": boolean_int_validation,
    },
    "redshift_interpolator_rebuild_when_settings_mismatch": {
        "value": True,
        "description": "Whether to rebuild the redshift interpolator when the config of the existing one don't match with the current config.",  # TODO: expand explanation
        "validation": boolean_int_validation,
    },
    "redshift_interpolator_stepsize": {
        "value": 0.001,
        "description": "Stepsize for the redshift interpolation.",  # TODO: expand explanation. Also consider if this is the best way
        "validation": float_or_int,
    },
    "redshift_interpolator_min_redshift_if_log": {
        "value": 1e-5,
        "description": "Minimum redshift for the redshift interpolator if using log spacing.",  # TODO: expand explanation. Also consider if this is the best way
        "validation": float_or_int,
    },
    "redshift_interpolator_min_redshift": {
        "value": 0,
        "description": "Minimum redshift for the redshift interpolator",  # TODO: expand explanation. Also consider if this is the best way
        "validation": float_or_int,
    },
    "redshift_interpolator_max_redshift": {
        "value": 50,
        "description": "Minimum redshift for the redshift interpolator",  # TODO: expand explanation. Also consider if this is the best way
        "validation": float_or_int,
    },
    "redshift_interpolator_use_log": {
        "value": True,
        "description": "Whether to interpolate in log redshift.",  # TODO: expand explanation
        "validation": boolean_int_validation,
    },
    "redshift_interpolator_data_output_filename": {
        # "value": os.path.join(
        #     os.path.dirname(os.path.abspath(__file__)), "interpolator_data_dict.p"
        # ),
        "value": None,
        "description": "Filename for the redshift interpolator object.",  # TODO: expand explanation. Also consider if this is the best way
        "validation": str,
    },
    ###################
    # Extra weights functionality
    "extra_weights_function": {
        "value": None,
        "description": "Function that calculates extra weights for each system or sub-ensemble. This functions should return a numpy array. The arguments of this function should be chosen from: 'config', 'time_value', 'convolution_instruction', 'data_dict' and the contents of 'extra_weights_function_additional_parameters'. For more explanation about this function see the convolution notebook.",
        "validation": callable_or_none_validation,
    },
    "extra_weights_function_additional_parameters": {
        "value": {},
        "description": "additional arguments that can be accessed by the extra_weights_function.",
        "validation": dict,
    },
    ###################
    # Multiprocessing settings
    "num_cores": {
        "value": 1,
        "description": "Number of cores to use to do the convolution",
        "validation": int,
    },
    "max_job_queue_size": {
        "value": 8,
        "description": "Max number of jobs in the multiprocessing queue for the convolution.",
        "validation": int,
    },
    ###################
    # custom convolution
    "custom_convolution_function": {
        "value": None,
        "description": "",  # TODO: expand
        "validation": callable_or_none_validation,
    },
    "custom_data_extraction_function": {
        "value": None,
        "description": "",  # TODO: expand
        "validation": callable_or_none_validation,
    },
    "include_custom_rates": {
        "value": False,
        "description": "Whether to include custom, user-specified, rates. See 'custom_rates_function'.",  # TODO: expand
        "validation": boolean_int_validation,
    },
    "custom_rates_function": {
        "value": None,
        "description": "Custom rate function used in the convolution.",  # TODO: expand
        "validation": callable_or_none_validation,
    },
    ###################
    # Logger
    "logger": {
        "value": logger,
        "description": "Logger object.",
        "validation": logger_validation,
    },
    ###################
    # Output processing settings
    "write_to_hdf5": {
        "value": True,
        "description": "Whether to write the pickle-files from the convolution back to the main hdf5 file",
        "validation": boolean_int_validation,
    },
    "remove_pickle_files": {
        "value": True,
        "description": "Flag whether to remove all the pickle files after writing them to the main hdf5 file",
        "validation": boolean_int_validation,
    },
    ###################
    # unsorted
    #
    "tmp_dir": {
        "value": "/tmp",
        "description": "Target directory for the tmp files.",  # TODO: expand explanation. Also consider if this is the best way
        "validation": str,
    },
    "cosmology": {
        "value": cosmo,
        "description": "Astropy cosmology used throughout the code. ",  # TODO: expand explanation
        # "validation": # TODO: add validation
    },
    "convolution_instructions": {
        "value": [{}],
        "description": "List of instructions for the convolution. ",  # TODO: expand explanation
        # "validation": # NOTE: validation handled with custom function
    },
    "input_filename": {
        "value": "",
        "description": "Full path to input hdf5 filename",
        "validation": existing_path_validation,
    },
    "output_filename": {
        "value": "",
        "description": "Full path to output hdf5 filename",
        "validation": str,
    },
    "check_convolution_config": {
        "value": True,
        "description": "Flag whether to validate the configuration dictionary before running the convolution code.",
        "validation": boolean_int_validation,
    },
    "delay_time_default_unit": {
        "value": u.yr,
        "description": "Default unit used for the delay-time data. NOTE: this can be overridden in data_dict column or layer entries.",
        "validation": unit_validation,
    },
    "yield_rate_unit": {
        "value": 1.0 / u.Msun,
        "description": "Unit used for the yield-rate data. NOTE: currently it is not possible to override this thoruh the data_dict column or layer entries.",
        "validation": unit_validation,
    },
}

# extract only values
default_convolution_config = {
    key: value["value"] for key, value in default_convolution_config_dict.items()
}

# extract only descriptions
default_convolution_config_descriptions = {
    key: value["description"] for key, value in default_convolution_config_dict.items()
}

#############
# Utilities to build the description table


def build_description_table(table_name, parameter_list, description_dict):
    """
    Function to create a table containing the description of the options
    """

    #
    indent = "   "

    # Get parameter list and parse descriptions
    parameter_list_with_descriptions = [
        [
            parameter,
            parse_description(description_dict=description_dict[parameter]),
        ]
        for parameter in parameter_list
    ]

    # Construct parameter list
    rst_table = """
.. list-table:: {}
{}:widths: 25, 75
{}:header-rows: 1
""".format(
        table_name, indent, indent
    )

    #
    rst_table += "\n"
    rst_table += indent + "* - Option\n"
    rst_table += indent + "  - Description\n"

    for parameter_el in parameter_list_with_descriptions:
        rst_table += indent + "* - {}\n".format(parameter_el[0])
        rst_table += indent + "  - {}\n".format(parameter_el[1])

    return rst_table


def parse_description(description_dict):
    """
    Function to parse the description for a given parameter
    """

    # Make a local copy
    description_dict = copy.copy(description_dict)

    ############
    # Add description
    description_string = "Description:\n   "

    # Clean description text
    description_text = description_dict["description"].strip()

    if description_text:
        description_text = description_text[0].capitalize() + description_text[1:]
        if description_text[-1] != ".":
            description_text = description_text + "."
    description_string += description_text

    ##############
    # Add unit (in latex)
    if "unit" in description_dict:
        if description_dict["unit"] != dimensionless_unit:
            description_string = description_string + "\n\nUnit: [{}].".format(
                description_dict["unit"].to_string("latex_inline")
            )

    ##############
    # Add default value
    if "value" in description_dict:
        # Clean
        if isinstance(description_dict["value"], str) and (
            "/home" in description_dict["value"]
        ):
            description_dict["value"] = "example path"

        # Write
        description_string = description_string + "\n\nDefault value:\n   {}".format(
            description_dict["value"]
        )

    ##############
    # Add validation
    if "validation" in description_dict:
        # Write
        description_string = description_string + "\n\nValidation:\n   {}".format(
            description_dict["validation"]
        )

    # Check if there are newlines, and replace them by newlines with indent
    description_string = description_string.replace("\n", "\n       ")

    return description_string


def write_default_settings_to_rst_file(options_defaults_dict, output_file: str) -> None:
    """
    Function that writes the descriptions of the grid options to an rst file

    Args:
        output_file: target file where the grid options descriptions are written to
    """

    ###############
    # Check input
    if not output_file.endswith(".rst"):
        msg = "Filename doesn't end with .rst, please provide a proper filename"
        raise ValueError(msg)

    ###############
    # construct descriptions dict
    descriptions_dict = {}
    for key, value in options_defaults_dict.items():
        descriptions_dict[key] = {}
        descriptions_dict[key]["description"] = value["description"]
        descriptions_dict[key]["value"] = value["value"]

        if "validation" in value:
            descriptions_dict[key]["validation"] = value["validation"]

    # separate public and private options
    public_options = [key for key in descriptions_dict if not key.startswith("_")]
    # private_options = [key for key in descriptions_dict if key.startswith("_")]

    ###############
    # Build description page text

    # Set up intro
    description_page_text = ""
    title = "Convolution options"
    description_page_text += title + "\n"
    description_page_text += "=" * len(title) + "\n\n"
    description_page_text += "The following chapter contains all Population code options, along with their descriptions."
    description_page_text += "\n\n"

    # Set up description table for the public options
    public_options_description_title = "Public options"
    public_options_description_text = public_options_description_title + "\n"
    public_options_description_text += (
        "-" * len(public_options_description_title) + "\n\n"
    )
    public_options_description_text += "In this section we list the public options for the population code. These are meant to be changed by the user.\n"
    public_options_description_text += build_description_table(
        table_name="Public options",
        parameter_list=sorted(public_options),
        description_dict=descriptions_dict,
    )
    description_page_text += public_options_description_text
    description_page_text += "\n\n"

    # # Set up description table for the private options
    # private_options_description_title = "Private internal variables"
    # private_options_description_text = private_options_description_title + "\n"
    # private_options_description_text += (
    #     "-" * len(private_options_description_title) + "\n\n"
    # )
    # private_options_description_text += "In this section we list the private internal parameters for the population code. These are not meant to be changed by the user.\n"
    # private_options_description_text += build_description_table(
    #     table_name="Private internal variables",
    #     parameter_list=sorted(private_options),
    #     description_dict=descriptions_dict,
    # )
    # description_page_text += private_options_description_text
    # description_page_text += "\n\n"

    ###############
    # write to file
    with open(output_file, "w") as f:
        f.write(description_page_text)
