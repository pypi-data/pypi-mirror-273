"""dialogue.py: Dialogue for the application."""


class Dialogue:
    """
    Dialogue for the application.

    Notes
    -----
    This class contains dialogue used throughout the application.
    By storing dialogue in a single location, it is easier to
    manage and update it. Dialogue should be defined as class
    attributes and should be named in uppercase with underscores
    separating words.
    """

    # Text
    INTRO_TEXT = """Welcome to Abraham!
Please ensure the input directory contains the correct directory structure, for example:

MTH1003 Ideas of Mathematical Proof
├── handbook
│   └── Module Specification.pdf
├── lectures
│   ├── 1.pdf
│   ├── 2.pdf
│   ├── 3.pdf
│   └── ...
├── papers
│   ├── 2021.pdf
│   ├── 2022.pdf
│   └── MOCK1.pdf
├── practicals
│   ├── 1.pdf
│   ├── 2.pdf
│   ├── 3.pdf
│   └── ...
└── tutorials
    ├── 1.pdf
    ├── 2.pdf
    ├── 3.pdf
    └── ...
"""
    EXIT_TEXT = "Exiting Abraham..."
    SETUP_TEXT = """Please enter the input directory path:"""

    # Input messages
    INPUT_PATH_TEXT = "Please enter the input directory path:"
    OUTPUT_PATH_TEXT = "Please enter the output directory path:"

    # Validation messages
    VALID_PATH_MESSAGE = "Valid path."

    # Error messages
    INVALID_PATH_ERROR = "Invalid path. Please try again."
    MISSING_DIRECTORY_ERROR = "Missing directory: {}"
    INVALID_STRUCTURE_ERROR = "Invalid directory structure. Please try again."
    DIRECTORY_NAMING_ERROR = "Invalid directory name: {}"
    MISSING_FILE_ERROR = "Missing file: {}"
    MESSY_DIRECTORY_ERROR = (
        "Messy directory: {}. Please ensure all files are in the correct directories."
    )

    PROCEED_TEXT = "Would you like to proceed anyway? [y/n]:"  # TODO: Add "proceed anyway" option
