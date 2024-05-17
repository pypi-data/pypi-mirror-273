"""type_annotations.py: Contains type annotations for the application."""

from typing import Any


class TypeAnnotations:
    """
    Type annotations for the application.

    Notes
    -----
    This class contains type annotations used throughout the application.
    By storing type annotations in a single location, it is easier to
    manage and update them. Type annotations should be defined as class
    attributes and should be named in uppercase with underscores
    separating words.
    """

    OVERVIEW_PAGE_DATA = dict[str, Any]
