"""module_data_structures.py: Data structures for the module generation."""

from typing import Any

from ..logs.setup_logging import setup_logging

module_data_structures_logger = setup_logging()


class Person:
    """A class to represent a person."""

    def __init__(self, name: str, email: str) -> None:
        """
        Constructs all the necessary attributes for the person object.

        Parameters
        ----------
        name : str
            The name of the person.
        email : str
            The email of the person.
        """
        self.name = name
        self.email = email


class Coordinator(Person):
    """
    A class to represent a coordinator.

    Parameters
    ----------
    Person : Person
        The person class.
    """

    def __init__(self, name: str, email: str) -> None:
        """
        Constructs all the necessary attributes for the coordinator object.

        Parameters
        ----------
        name : str
            The name of the coordinator.
        email : str
            The email of the coordinator.
        """
        super().__init__(name, email)


class ModuleComponent:
    """A class to represent a module component."""

    def __init__(self, max_percentage: float, current_percentage: float) -> None:
        """
        Constructs all the necessary attributes for the module component object.

        Parameters
        ----------
        max_percentage : float
            The maximum percentage of the module component.
        current_percentage : float
            The current grade of the module component.
        """
        self.percentage = max_percentage
        self.current = current_percentage


class Portfolio(ModuleComponent):
    """
    A class to represent a portfolio.

    Parameters
    ----------
    ModuleComponent : ModuleComponent
        The module component class.
    """

    def __init__(self, maximum_percentage: float, current_percentage: float) -> None:
        """
        Constructs all the necessary attributes for the portfolio object.

        Parameters
        ----------
        maximum_percentage : float
            The maximum percentage of the portfolio.
        current : float
            The current grade of the portfolio.
        """
        super().__init__(maximum_percentage, current_percentage)


class FinalExams(ModuleComponent):
    """
    A class to represent final exams.

    Parameters
    ----------
    ModuleComponent : ModuleComponent
        The module component class.
    """

    def __init__(self, maximum_percentage: float, current_percentage: float) -> None:
        """
        Constructs all the necessary attributes for the final exams object.

        Parameters
        ----------
        maximum_percentage : float
            The maximum percentage of the final exams.
        current_percentage : float
            The current grade of the final exams.
        """
        super().__init__(maximum_percentage, current_percentage)


class Note:
    """A class to represent a note."""

    def __init__(self, title: str, description: str, content: str | None = None) -> None:
        """
        Constructs all the necessary attributes for the note object.

        Parameters
        ----------
        title : str
            The title of the note.
        description: str
            The description of the note.
        content: str, optional
            The content of the note, by default None.
        """
        self.title = title
        self.description = description
        self.content: str | None = content if content else self.add_content()

    def add_content(self) -> str | None:
        """
        Add content to the note.

        Returns
        -------
        str | None
            The content of the note.

        Notes
        -----
        Uses an LLM to add content to the note.
        """
        return None  # TODO: Implement LLM note generation


class Subsection:
    """A class to represent a subsection."""

    def __init__(self, title: str) -> None:
        """
        Constructs all the necessary attributes for the subsection object.

        Parameters
        ----------
        title : str
            The title of the subsection.
        """
        self.title = title
        self.notes: list[Note] = []

    def add_note(self, note: Note) -> None:
        """
        Add a note to the subsection.

        Parameters
        ----------
        note : Note
            The note to add to the subsection.
        """
        self.notes.append(note)


class Section:
    """A class to represent a section."""

    def __init__(self, title: str) -> None:
        """
        Constructs all the necessary attributes for the section object.

        Parameters
        ----------
        title : str
            The title of the section.
        """
        self.title = title
        self.subsections: list[Subsection] = []

    def add_subsection(self, subsection: Subsection) -> None:
        """
        Add a subsection to the section.

        Parameters
        ----------
        subsection : Subsection
            The subsection to add to the section.
        """
        self.subsections.append(subsection)


class Module:
    """A class to represent a module."""

    def __init__(self, coordinator: Coordinator, title: str):
        """
        Constructs all the necessary attributes for the module object.

        Parameters
        ----------
        coordinator : Coordinator
            The coordinator of the module.
        title : str
            The title of the module.
        """
        self.coordinator = coordinator
        self.title = title
        self.components: dict[str, ModuleComponent] = {}
        self.sections: list[Section] = []
        self.learning_outcomes: list[tuple[str, bool]] = []
        self.recommended_reading: list[dict[str, str]] = []

    def add_component(self, name: str, component: ModuleComponent) -> None:
        """
        Add a component to the module.

        Parameters
        ----------
        name : str
            The name of the component.
        component : ModuleComponent
            The component to add to the module.
        """
        self.components[name] = component

    def add_section(self, section: Section) -> None:
        """
        Add a section to the module.

        Parameters
        ----------
        section : Section
            The section to add to the module.
        """
        self.sections.append(section)

    def add_learning_outcome(self, outcome: str, completion: bool) -> None:
        """
        Add a learning outcome to the module.

        Parameters
        ----------
        outcome : str
            The learning outcome.
        completion : bool
            Whether the learning outcome has been completed.
        """
        self.learning_outcomes.append((outcome, completion))

    def add_recommended_reading(self, title: str, author: str, year: str) -> None:
        """
        Add recommended reading to the module.

        Parameters
        ----------
        title : str
            The title of the recommended reading.
        author : str
            The author of the recommended reading.
        year : str
            The year of the recommended reading.
        """
        self.recommended_reading.append({"title": title, "author": author, "year": year})

    def get_data_dictionary(self) -> dict[str, Any]:
        """
        Get the data dictionary for the module.

        Returns
        -------
        dict[str, Any]
            The data dictionary for the module.
        """
        return {
            "title": self.title,
            "coordinator": {
                "name": self.coordinator.name,
                "email": self.coordinator.email,
            },
            "components": {
                component_name: {
                    "percentage": component.percentage,
                    "current": component.current,
                }
                for component_name, component in self.components.items()
            },
            "learning_outcomes": self.learning_outcomes,
            "recommended_reading": self.recommended_reading,
            "sections": [
                {
                    "title": section.title,
                    "subsections": [
                        {
                            "title": subsection.title,
                            "notes": [
                                {
                                    "title": note.title,
                                    "description": note.description,
                                }
                                for note in subsection.notes
                            ],
                        }
                        for subsection in section.subsections
                    ],
                }
                for section in self.sections
            ],
        }


"""
Module
    coordinator
        .name = ""
        .email = ""
    module
        .title = ""
        components
            .portfolio = [percentage, current]
            .final_exams = [percentage, current]
        sections
            .title = ""
                subsections
                    .title = ""
                    .notes = {link_title, description}
    learning_outcomes = {outcome, completion}
    recommended_reading = {title, author, year}

overview_template_name = Paths.OVERVIEW_TEMPLATE_NAME
overview_path = output_path / module_title
"""
