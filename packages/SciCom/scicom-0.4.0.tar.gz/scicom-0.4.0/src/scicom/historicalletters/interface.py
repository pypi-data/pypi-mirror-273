"""Define the solara interface to run and control the HistoricalLetters model."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import mesa

import contextily as cx
import matplotlib.pyplot as plt
import numpy as np
import solara
from matplotlib import colors
from mesa.experimental.jupyter_viz import JupyterViz

from scicom.historicalletters.agents import (
        RegionAgent,
        SenderAgent,
)
from scicom.historicalletters.model import HistoricalLetters
from scicom.historicalletters.server import (
        topic_draw,
)

model_params = {
    "population": {
        "type": "SliderInt",
        "value": 50,
        "label": "Number of agents",
        "min": 10,
        "max": 200,
        "step": 10,
    },
    "useSocialNetwork": {
        "type": "Select",
        "value": False,
        "label": "Choose if an initial social network exists.",
        "values": [True, False],
    },
    "useActivation": {
        "type": "Select",
        "value": False,
        "label": "Choose if agents have heterogeneous acitvations.",
        "values": [True, False],
    },
    "similarityThreshold": {
        "type": "SliderFloat",
        "value": 0.5,
        "label": "Threshold for similarity of topics.",
        "min": 0.0,
        "max": 1.0,
        "step": 0.1,
    },
    "moveRange": {
        "type": "SliderFloat",
        "value": 0.05,
        "label": "Range defining targets for movements.",
        "min": 0.0,
        "max": 0.5,
        "step": 0.1,
    },
    "letterRange": {
        "type": "SliderFloat",
        "value": 0.2,
        "label": "Range for sending letters.",
        "min": 0.0,
        "max": 0.5,
        "step": 0.1,
    },
}

def has_main_topic(data:dict) -> tuple:
        """Return weighted average topics of agents in region."""
        if len(data) > 0:
            topics = [y[0] for x, y in data.items()]
            total = [y[1] for x, y in data.items()]
            weight = [x / sum(total) for x in total] if sum(total) > 0 else [1 / len(topics)] * len(topics)
            mixed_colors = np.sum([np.multiply(weight[i], topics[i]) for i in range(len(topics))], axis=0)
            return np.subtract((1, 1, 1), mixed_colors)
        return (0.5, 0.5, 0.5)


def make_geospace(model:mesa.Model, agent_portrayal:dict | None = None) -> solara.FigureMatplotlib:
    """Create the geo figure."""
    space_fig, space_ax = plt.subplots()
    # _draw_layers(model.space, space_ax)
    _draw_agents(model.space, space_ax)
    space_ax.set_axis_off()
    solara.FigureMatplotlib(space_fig, format="png")


def _draw_layers(space:mesa.Space, space_ax:plt.Axes) -> None:
    """Draw layers."""


def _draw_agents(space:mesa.Space, space_ax:plt.Axes) -> plt.Axes:
    """Draw the Region and SenderAgents."""
    region_agents = space.get_agents_as_GeoDataFrame(agent_cls=RegionAgent)
    region_agents["averageTopic"] = region_agents["senders_in_region"].apply(
        lambda x: colors.to_hex(has_main_topic(x)),
    )

    region_agents.plot(column="averageTopic", alpha=0.5, ax=space_ax)

    person_agents = space.get_agents_as_GeoDataFrame(agent_cls=SenderAgent)
    person_agents["color"] = person_agents["topicVec"].apply(
        lambda x: colors.to_hex(x),
    )
    person_agents.plot(column="color", markersize=1, ax=space_ax)

    space_ax.set_xlim([-1e6, 4e6])
    space_ax.set_ylim([4.3e6, 9.3e6])
    cx.add_basemap(space_ax, source=cx.providers.CartoDB.Positron)



page = JupyterViz(
    HistoricalLetters,
    model_params,
    measures=["Movements", "Clusters", "Letters"],
    name="Historical Letters ABM",
    agent_portrayal=topic_draw,
    space_drawer=make_geospace,
)
