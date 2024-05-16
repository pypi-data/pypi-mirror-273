"""Solara interface for all simulations."""
from pathlib import Path

import solara

from scicom.historicalletters.interface import page as historical_letters_page
from scicom.knowledgespread.interface import page as knowledgespread_page


@solara.component
def Home():
    # load about markdown file in the same directory
    with Path.open(Path(Path(__file__).parent.parent.parent.resolve(), "README.md")) as readmefile:
        return solara.Markdown("\n".join(readmefile.readlines()))


@solara.component
def historicalletters():
    return historical_letters_page


@solara.component
def knowledgespread():
    return knowledgespread_page


routes = [
    solara.Route(path="/", component=Home, label="Simulation methods"),
    solara.Route(
        path="historicalletters", component=historicalletters, label="Historical Letters",
    ),
    solara.Route(
        path="knowledgespread",
        component=knowledgespread,
        label="Knowledge Spread",
    ),
]
