""" Banjara textual interface.

"""

from textual.app import (
    App,
    ComposeResult
)

from textual.containers import (
    Container,
    Horizontal,
    Grid,
)

from textual.widgets import (
    Header,
    Footer,
)

from .overview import Dashboard


class BanjaraUI(App):

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("ctrl+q", "quit", "Quit")
    ]

    # Decorative constants
    TITLE = "Banjara"
    SUB_TITLE = "a pretty terminal POS"

    # def on_mount(self) -> None:

    def compose(self) -> ComposeResult:
        """ Create child widgets for the app.
        """
        yield Header()
        yield Dashboard()
        yield Footer()

    def action_toggle_dark(self) -> None:
        """ An action to toggle dark mode.
        """
        self.dark = not self.dark


def main():
    app = BanjaraUI()
    app.run()


if __name__ == "__main__":
    main()
