"""

"""
from textual.app import (
    ComposeResult
)

from textual.containers import (
    Container,
    Grid,
)

from textual.widgets import (
    Placeholder,
    Sparkline,
)


class Dashboard(Container):

    CSS_PATH = "banjara.tcss"

    data = [1, 2, 2, 1, 1, 4, 3, 1, 1, 8, 8, 2]

    def compose(self) -> ComposeResult:
        """ Create child widgets for the app.
        """
        yield Sparkline(
            self.data,
            summary_function=max,
        )
