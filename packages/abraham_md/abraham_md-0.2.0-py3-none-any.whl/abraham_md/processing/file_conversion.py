"""file_conversion.py: Contains functions for converting files."""

import json
import os
from datetime import timedelta
from pathlib import Path
from time import time
from typing import Callable

import requests

from ..config.constants import Constants
from ..logs.setup_logging import setup_logging

file_conversion_logger = setup_logging()


def process_files(process_function: Callable, file_list: list[Path]) -> None:
    """
    Process a list of files using a provided function.

    Parameters
    ----------
    process_function : Callable
        The function to process each file.
    file_list : list[Path]
        A list of paths to the files to process.

    Notes
    -----
    This function processes a list of files using a provided function.
    It logs the progress of the file processing and the estimated time remaining.
    """
    total_files = len(file_list)
    start_time = time()
    file_conversion_logger.info("Starting file processing...")

    for i, file in enumerate(file_list):
        process_function(file)

        current_time = time()
        elapsed_time = current_time - start_time
        files_processed = i + 1
        avg_time_per_file = elapsed_time / files_processed
        remaining_files = total_files - files_processed
        estimated_time_left = avg_time_per_file * remaining_files
        formatted_time_left = str(timedelta(seconds=int(estimated_time_left)))
        progress = files_processed / total_files

        # Create a progress bar with 20 segments
        progress_bar = "#" * int(progress * 20) + "-" * (20 - int(progress * 20))

        file_conversion_logger.info(
            f"Progress: [{progress_bar}] {progress * 100:.2f}% Complete - "
            f"Estimated time remaining: {formatted_time_left}\r"
        )

    file_conversion_logger.info("All files have been processed.")


def list_files(directory: Path, file_extension: str) -> list[tuple[Path, str]]:
    """
    List all files in a directory with a specific file extension.

    Parameters
    ----------
    directory : Path
        The path to the directory to list files from.
    file_extension : str
        The file extension to filter files by.

    Returns
    -------
    list[tuple[Path, str]]
        A list of tuples containing the file path and filename.

    Raises
    ------
    NotADirectoryError
        If the input directory is not a directory.

    Notes
    -----
    This function lists all files in a directory with a specific file extension.
    """
    if not os.path.isdir(directory):
        raise NotADirectoryError(f"{directory} is not a directory.")

    file_list: list[tuple[Path, str]] = []

    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = Path(dirpath) / filename
            if file_path.suffix == file_extension:
                file_list.append((file_path, filename))

    return file_list


def pdf_to_markdown(input_path: Path) -> Path:
    """
    Convert a PDF file to Markdown using the Mathpix API.

    Parameters
    ----------
    input_path : Path
        The path to the PDF file to convert.

    Returns
    -------
    Path
        The path to the Markdown file that was created.

    Exceptions
    ----------
    requests.HTTPError
        If the Mathpix API returns an error.

    Notes
    -----
    This function converts a PDF file to Markdown using the Mathpix API.
    It writes the Markdown output to a file with the same name as the input file,
    but with a `.md` extension.
    """
    output_path = input_path.with_suffix(Constants.MATHPIX_CONVERSION_SUFFIX)

    headers = {
        "app_id": Constants.MATHPIX_APP_ID,
        "app_key": Constants.MATHPIX_APP_KEY,
    }

    intial_post = requests.post(
        Constants.MATHPIX_ENDPOINT,
        headers=headers,
        data={"options_json": json.dumps(Constants.MATHPIX_OPTIONS)},
        files={"file": open(input_path, "rb")},
    )

    request_id = intial_post.json()["pdf_id"]

    while True:
        response = requests.get(f"{Constants.MATHPIX_ENDPOINT}/{request_id}", headers=headers)
        response_data = response.json()

        if "error" in response_data:
            raise requests.HTTPError(response_data["error"])

        if response_data["status"] == "error":
            raise requests.HTTPError(response_data["error"])

        if response_data["status"] == "completed":
            break

    markdown_url = f"{Constants.MATHPIX_ENDPOINT}/{request_id}{Constants.MATHPIX_CONVERSION_SUFFIX}"
    markdown_response = requests.get(markdown_url, headers=headers)

    with open(output_path, "w") as markdown_file:
        markdown_file.write(markdown_response.text)

    return output_path
