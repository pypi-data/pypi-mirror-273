"""path_validation.py: Validate paths for the application."""

import re
from pathlib import Path

from ..config.dialogue import Dialogue
from ..config.structures import Structures
from ..logs.setup_logging import setup_logging

path_validation_logger = setup_logging()


def validate_directory_structure(path: Path) -> bool:
    """
    Validate the directory structure of the input path.

    Parameters
    ----------
    path : Path
        The input path to validate.

    Returns
    -------
    bool
        True if the directory structure is valid, False otherwise.

    Notes
    -----
    This function validates the directory structure of the input path
    by checking if the path is named after a module and if the sub-directories
    and files are named correctly.
    """
    # check path is named after module
    if not re.match(Structures.INPUT_DIRECTORY_STRUCTURE_REGEX["module"], path.name):
        path_validation_logger.error(Dialogue.MISSING_DIRECTORY_ERROR.format("module"))
        return False

    # check sub-directories
    for sub_directory in path.iterdir():
        if sub_directory.is_dir():
            if sub_directory.name not in Structures.INPUT_DIRECTORY_STRUCTURE_REGEX.keys():
                path_validation_logger.error(
                    Dialogue.DIRECTORY_NAMING_ERROR.format(sub_directory.name)
                )
                return False

            # check files in sub-directory
            for file in sub_directory.iterdir():
                if not re.match(
                    Structures.INPUT_DIRECTORY_STRUCTURE_REGEX[sub_directory.name], file.name
                ):
                    path_validation_logger.error(Dialogue.MISSING_FILE_ERROR.format(file.name))
                    return False
        else:
            path_validation_logger.error(Dialogue.MESSY_DIRECTORY_ERROR.format(sub_directory.name))
            return False

    return True


def validate_input_path(path: Path) -> bool:
    """
    Validate the input path for the application.

    Parameters
    ----------
    path : Path
        The input path to validate.

    Returns
    -------
    bool
        True if the path is valid, False otherwise.

    Notes
    -----
    This function validates the input path for the application,
    by checking if the path exists and its sub-directory structure
    is valid.
    """
    if not path.is_dir():
        path_validation_logger.error(Dialogue.INVALID_PATH_ERROR)
        return False

    if not validate_directory_structure(path):
        path_validation_logger.error(Dialogue.INVALID_STRUCTURE_ERROR)
        return False

    return True
