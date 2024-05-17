"""file_interaction.py: File interaction functions for Abraham."""

from pathlib import Path
from typing import Any, Callable

from jinja2 import Environment, FileSystemLoader

from ..config.constants import Constants
from ..config.paths import Paths
from ..logs.setup_logging import setup_logging
from .llm_integration import prompt_gpt

file_interaction_logger = setup_logging()


def fetch_information(
    to_fetch: str,
    process_to_use: str,
    prompt: str = Constants.FETCH_SYSTEM_PROMPT,
    file_path: Path | None = None,
    prompt_llm: Callable = prompt_gpt,
) -> str:
    """
    Fetch information from a file using an LLM.

    Parameters
    ----------
    to_fetch : str
        The information to fetch.
    process_to_use : str
        The process to use, either "llm" or "input".
    prompt : str
        The prompt to use for input, by default Constants.FETCH_SYSTEM_PROMPT.
    file_path : Path, optional
        The path to the file to fetch information from, by default None.
    prompt_llm : Callable
        The LLM function to prompt with, by default prompt_gpt.

    Returns
    -------
    str
        The fetched information.

    Examples
    --------
    >>> fetch_information("example.pdf", ["module name", "module coordinator name"])
    ["Module Name: Example Module", "Module Coordinator Name: John Doe"]

    Notes
    -----
    This function fetches information from a file using an LLM.
    """
    if process_to_use not in ["llm", "input"]:
        file_interaction_logger.error(f"Process '{process_to_use}' not recognised.")
        raise ValueError(f"Process '{process_to_use}' not recognised.")

    if process_to_use == "input" and not prompt:
        file_interaction_logger.error("Prompt not provided.")
        raise ValueError("Prompt not provided.")

    if process_to_use == "llm" and not file_path:
        file_interaction_logger.error("File path not provided.")
        raise ValueError("File path not provided.")

    fetched_information: str

    if process_to_use == "llm" and file_path is not None:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                file_text = file.read()
        except FileNotFoundError as e:
            file_interaction_logger.error(f"File '{file_path}' not found.")
            raise e
        except UnicodeDecodeError as e:
            file_interaction_logger.error(f"File '{file_path}' is not a text file.")
            raise e
        except Exception as e:
            file_interaction_logger.error(f"An error occurred while opening '{file_path}': {e}")
            raise e

        if prompt == Constants.FETCH_SYSTEM_PROMPT:
            fetched_information = prompt_llm(file_text, prompt.format(information=to_fetch))
        else:
            fetched_information = prompt_llm(file_text, prompt)
    elif process_to_use == "input":
        fetched_information = input(f"{to_fetch}: ")
    else:
        raise ValueError("An error occurred while fetching information.")

    return fetched_information


def generate_markdown(template_name: str, output_path: Path, data: dict[str, Any]) -> None:
    """
    Generate a Markdown file using a template.

    Parameters
    ----------
    template_name : str
        The name of the template to use.
    output_path : Path
        The path to save the generated Markdown file.
    data : dict[str, Any]
        The data to render the template with.

    Examples
    --------
    >>> generate_markdown("example.md", "example.md", {"title": "Example Title"})

    Notes
    -----
    This function generates a Markdown file using a template.
    """
    file_interaction_logger.debug(f"Generating Markdown file at '{output_path}'.")

    template_objects = Environment(loader=FileSystemLoader(Paths.TEMPLATES_PATH))
    template_object = template_objects.get_template(template_name)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(template_object.render(data))
