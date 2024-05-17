"""module_logic.py: Logic for the module generation."""

from ..logs.setup_logging import setup_logging
from ..processing.file_interaction import fetch_information
from .module_data_structures import (
    Coordinator,
    FinalExams,
    Module,
    Note,
    Portfolio,
    Section,
    Subsection,
)

module_logic_logger = setup_logging()


def generate_module() -> Module:
    """Generate the module."""
    # Create the module object
    module = Module(
        Coordinator(
            fetch_information("Module Co-ordinator Name", "input"),
            fetch_information("Module Co-ordinator Email", "input"),
        ),
        fetch_information("Module Name", "input"),
    )

    # Add the components to the module
    module.add_component(
        "portfolio",
        Portfolio(
            float(fetch_information("Portfolio Max Percentage", "input")),
            float(fetch_information("Portfolio Current Percentage", "input")),
        ),
    )
    module.add_component(
        "final exams",
        FinalExams(
            float(fetch_information("Final Exams Max Percentage", "input")),
            float(fetch_information("Final Exams Current Percentage", "input")),
        ),
    )

    # Add the learning outcomes to the module.
    for _ in range(int(fetch_information("Number of Learning Outcomes", "input")) - 1):
        module.add_learning_outcome(
            fetch_information("Learning Outcome", "input"),
            bool(fetch_information("Learning Outcome Completion", "input")),
        )

    # Add the recommended reading to the module.
    for _ in range(int(fetch_information("Number of Recommended Books", "input")) - 1):
        module.add_recommended_reading(
            fetch_information("Book Title", "input"),
            fetch_information("Book Author", "input"),
            fetch_information("Book Year", "input"),
        )

    # Add the notes to the module.
    section_titles: list[str] = fetch_information("Module Outline", "input").split("\n")

    for section_title in section_titles:
        section_object = Section(section_title)
        subsection_titles: list[str] = fetch_information("Subsection Titles", "input").split("\n")

        for subsection_title in subsection_titles:
            subsection_object = Subsection(subsection_title)
            note_titles_and_descriptions: list[str] = fetch_information(
                "Note Titles and Descriptions", "input"
            ).split("\n")

            for note_title_and_description in note_titles_and_descriptions:
                note_title, note_description = note_title_and_description.split(":")
                note_object = Note(note_title, note_description)

                subsection_object.add_note(note_object)

            section_object.add_subsection(subsection_object)

        module.add_section(section_object)

    return module
