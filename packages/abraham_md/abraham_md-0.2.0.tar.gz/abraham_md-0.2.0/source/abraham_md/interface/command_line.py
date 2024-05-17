"""command_line.py: Command line interface for the application."""

from pathlib import Path

from ..config.dialogue import Dialogue
from ..logs.setup_logging import setup_logging
from ..validation.path_validation import validate_input_path

cli_interface_logger = setup_logging()


def intro_text() -> None:
    """
    Display the introduction text for the application.

    Notes
    -----
    This function displays the introduction text for the application.
    """
    cli_interface_logger.info(Dialogue.INTRO_TEXT)


def fetch_input_path() -> Path:
    """
    Fetch the input directory path from the user.

    Returns
    -------
    Path
        The input directory path.

    Exceptions
    ----------
    FileNotFoundError
        Raised when the input path is invalid.

    Notes
    -----
    This function prompts the user to enter the input directory path.
    The input path is then validated to ensure it exists and contains
    the correct directory structure.
    """
    cli_interface_logger.info(Dialogue.SETUP_TEXT)
    cli_interface_logger.info(Dialogue.INPUT_PATH_TEXT)
    input_directory = input()

    try:
        input_path = Path(input_directory)
        input_path_validity = validate_input_path(input_path)

        if input_path_validity is True:
            return input_path
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        cli_interface_logger.error(Dialogue.INVALID_PATH_ERROR)
        return fetch_input_path()


def fetch_output_path() -> Path:
    """
    Fetch the output directory path from the user.

    Returns
    -------
    Path
        The output directory path.

    Notes
    -----
    This function prompts the user to enter the output directory path.
    """
    cli_interface_logger.info(Dialogue.OUTPUT_PATH_TEXT)
    output_directory = input()
    return Path(output_directory)
