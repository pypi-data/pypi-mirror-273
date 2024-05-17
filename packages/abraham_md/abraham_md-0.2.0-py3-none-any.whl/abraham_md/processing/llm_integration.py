"""llm_integration.py: Contains functions for integrating with LLMs."""

from typing import cast

from openai import OpenAI

from ..config.constants import Constants
from ..logs.setup_logging import setup_logging

llm_logger = setup_logging()


def prompt_gpt(
    user_message: str,
    system_message: str = "You are a helpful assistant.",
    api_key: str | None = Constants.OPENAI_API_KEY,
    model: str = "gpt-3.5-turbo",
) -> str | None:
    """
    Prompt an OpenAI GPT model with a user message.

    Parameters
    ----------
    user_message : str
        The message to prompt the model with.
    system_message : str, optional
        The system message to prompt the model with, by default "You are a helpful assistant."
    api_key : str | None, optional
        The OpenAI API key, by default Constants.OPENAI_API_KEY
    model : str, optional
        The OpenAI model to use, by default "gpt-3.5-turbo"

    Returns
    -------
    str | None
        The response from the model, or None if an error occurred.

    Examples
    --------
    >>> prompt_gpt("What is the capital of France?")
    'The capital of France is Paris.'

    Notes
    -----
    This function prompts an OpenAI GPT model with a user message.
    """
    if not api_key:
        llm_logger.error("OpenAI API key not found.")
        return None

    try:
        llm_logger.debug("Creating OpenAI client.")
        client = OpenAI(api_key=api_key)

        llm_logger.debug(f"Prompting the OpenAI client with: '{user_message}'.")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
        )

        llm_logger.debug(f"Response received: '{response.choices[0].message.content}'.")
        return cast(str, response.choices[0].message.content)
    except Exception as e:
        llm_logger.error(f"Error: {e}")
        return None
