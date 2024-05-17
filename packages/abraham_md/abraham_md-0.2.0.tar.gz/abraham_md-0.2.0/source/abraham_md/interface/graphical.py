"""graphical.py: Graphical user interface for the application."""

from pathlib import Path

# TODO: Implement the graphical user interface for the application.
# TODO: Add kivy to the requirements.
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.textinput import TextInput

from ..config.dialogue import Dialogue
from ..logs.setup_logging import setup_logging
from ..validation.path_validation import validate_input_path

gui_interface_logger = setup_logging()


class AbrahamApp(App):
    """
    Main class for the application.

    Notes
    -----
    This class is the main class for the application.
    """

    def build(self) -> BoxLayout:
        """
        Build the application layout.

        Returns
        -------
        BoxLayout
            The application layout.

        Notes
        -----
        This function builds the application layout.
        """
        self.title = "Abraham"
        self.layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        self.intro_label = Label(text=Dialogue.INTRO_TEXT)
        self.layout.add_widget(self.intro_label)

        self.input_label = Label(text=Dialogue.SETUP_TEXT)
        self.layout.add_widget(self.input_label)

        self.input_box = TextInput(multiline=False, write_tab=False)
        self.layout.add_widget(self.input_box)

        self.submit_button = Button(text="Submit")
        self.submit_button.bind(on_press=self._validate_input_path)
        self.layout.add_widget(self.submit_button)

        self.progress_bar = ProgressBar(max=100)
        self.layout.add_widget(self.progress_bar)

        self.output_label = Label(text="")
        self.layout.add_widget(self.output_label)

        return self.layout

    def _update_progress(self, dt: float) -> None:
        """
        Update the progress bar.

        Parameters
        ----------
        dt : float
            The time interval.

        Notes
        -----
        This function updates the progress bar.
        """
        if self.progress_bar.value < 100:
            self.progress_bar.value += 1
        else:
            Clock.unschedule(self._update_progress)
            self.output_label.text = Dialogue.VALID_PATH_MESSAGE
            self.input_box.disabled = False
            self.submit_button.disabled = False

    def _validate_input_path(self, instance: Button) -> None:
        """
        Validate the input path entered by the user.

        Parameters
        ----------
        instance : Button
            The button instance.

        Notes
        -----
        This function validates the input path entered by the user.
        """
        input_directory = self.input_box.text
        try:
            input_path = Path(input_directory)
            input_path_validity = validate_input_path(input_path)

            if input_path_validity is True:
                self.output_label.text = Dialogue.VALID_PATH_MESSAGE
                self.progress_bar.value = 0
                self.input_box.disabled = True
                self.submit_button.disabled = True
                Clock.schedule_interval(self._update_progress, 0.05)
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            self.output_label.text = Dialogue.INVALID_PATH_ERROR
