"""A visualization interface for HistoricalLetters using the older visualization option of mesa."""
import mesa
import mesa_geo as mg
from matplotlib import colors
from mesa.visualization.modules import ChartVisualization

from scicom.historicalletters.agents import RegionAgent, SenderAgent
from scicom.historicalletters.model import HistoricalLetters

model_params = {
    "population": mesa.visualization.Slider(
        "Number of persons",
        50, 10, 100, 10,
        description="Choose how many senders to include in the model.",
    ),
    "useSocialNetwork": mesa.visualization.Checkbox(
        "Create initial social network of agents",
        False,
    ),
    "useActivation": mesa.visualization.Checkbox(
        "Use heterogenous activations",
        False,
    ),
    "similarityThreshold": mesa.visualization.Slider(
        "Similarity threshold",
        0.5, 0.0, 1.0, 0.1,
        description="Choose how similar two agents topics have to be, to send a letter.",
    ),
    "moveRange": mesa.visualization.Slider(
        "Range for moving position</br>(% of mean agent distances)",
        0.01, 0.00, 0.5, 0.05,
        description="Choose the visibility range for finding potential locations to move to.",
    ),
    "letterRange": mesa.visualization.Slider(
        "Range for letter sending</br>(% of mean agent distances)",
        0.2, 0.1, 1.0, 0.1,
        description="Choose the visibility range for finding potential recipients.",
    ),
}


def topic_draw(agent:mg.GeoAgent) -> dict:
    """Define visualization strategies for agents.

    Region agents get the main color as a mean of
    all region agents topic vectors.

    Sender agetns have the color of their current
    topic vector.
    """
    portrayal = {}
    if isinstance(agent, RegionAgent):
        color = colors.to_hex(agent.has_main_topic())
        portrayal["color"] = color
    elif isinstance(agent, SenderAgent):
        colortuple = set(agent.topicVec)
        portrayal["radius"] = 5
        portrayal["shape"] = "circle"
        portrayal["color"] = colors.to_hex(colortuple)
        portrayal["description"] = str(agent.unique_id)
    return portrayal

map_element = mg.visualization.MapModule(
    portrayal_method=topic_draw,
    view=[52, 12],
    zoom=4,
    map_width=700,
    map_height=500,
)

chart = ChartVisualization.ChartModule(
    [
        {"Label": "Movements", "Color": "red"},
        {"Label": "Clusters", "Color": "black"},
        {"Label": "Letters", "Color": "green"},
    ],
    data_collector_name="datacollector",
)


server = mesa.visualization.ModularServer(
    HistoricalLetters,
    [map_element, chart],
    "Historical Letters",
    model_params,
)
