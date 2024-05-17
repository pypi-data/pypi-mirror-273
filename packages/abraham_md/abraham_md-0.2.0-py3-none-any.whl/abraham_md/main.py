"""main.py: Called when the package is run as a script."""

from .config.constants import Constants
from .config.dialogue import Dialogue
from .config.paths import Paths
from .generation.module_logic import generate_module
from .interface.command_line import fetch_input_path, fetch_output_path, intro_text
from .logs.setup_logging import setup_logging
from .processing.file_conversion import list_files, pdf_to_markdown, process_files
from .processing.file_interaction import generate_markdown

main_logger = setup_logging()

"""
TEMPORARY RAMBLINGS:
--------------------

# TODO: Implement past and predicted exam papers
CONVERSATION WITH GPT-3.5-TURBO AS IF TAKING INPUT FROM USER

TODO: PROJECT FLOW
PDF -> MD -> Abstraction -> Elaboration -> MD (-> APKG, PDF)
Done: PDF -> MD -> Abstraction

TODO: FETCH REQUIRED DATA
module name
module coordinator name
module coordinator email
assessment weighting percentages
learning outcomes
module outline
recommended reading

TODO: ARGUMENT PARSING
input as arguments, e.g. abraham_md --input <path> --output <path>
instructions for usage as argument, e.g. abraham_md --help
no arguments, e.g. abraham_md, return error message prompting user to use --help
optional arguments, e.g. verbosity level (--verbose), log file (--log), etc.
allow single letter arguments, e.g. -i, -o, -h, -v, -l, etc.

TODO: GUI
when ported to gui, use kivy/kivyMD and file choosers/checkboxes for input: the
gui should replace command line interface, not run alongside it - but keep optional
argument parsing for verbosity, log file, etc.
"""


def main() -> None:
    """
    Main function for the application.

    Notes
    -----
    This function is the entry point for the application.
    """
    try:
        # Fetch input and output paths
        intro_text()
        input_path = fetch_input_path()
        output_path = fetch_output_path()

        # List files in input directory
        file_tuples = list_files(input_path, Constants.TO_CONVERT_EXTENSION)
        file_paths = [file_tuple[0] for file_tuple in file_tuples]

        # Process files in input directory, converting PDFs to Markdown
        process_files(pdf_to_markdown, file_paths)

        # Generate the module
        module = generate_module()
        module_data = module.get_data_dictionary()

        # Generate the markdown files
        template_tuples = list_files(Paths.TEMPLATES_PATH, Constants.TEMPLATE_EXTENSION)
        template_names: list[str] = [template_tuple[1] for template_tuple in template_tuples]
        for template_name in template_names:
            generate_markdown(
                template_name,
                output_path / template_name.replace(".j2", ""),
                module_data,
            )

    except KeyboardInterrupt:
        print("\n")
        main_logger.info(Dialogue.EXIT_TEXT)


if __name__ == "__main__":
    main()
