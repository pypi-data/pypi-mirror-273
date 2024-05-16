"""Test server initialization."""

from scicom.historicalletters.model import (
    HistoricalLetters,
)
from scicom.historicalletters.server import (
    server,
    topic_draw,
)

#####
# Test server setup
#####

def test_server() -> None:
    """Test server launch."""
    assert server.model_name == "Historical Letters"
    assert isinstance(server.description, str)


def test_region_draw() -> None:
    """Test drawing a region."""
    model = HistoricalLetters(15)
    region = model.regions[10]
    agent = model.schedule.agents[5]
    pot = topic_draw(region)
    color = pot.get("color")
    assert isinstance(color, str)
    assert color.startswith("#")
    pot2 = topic_draw(agent)
    for val in ["radius", "shape", "color", "description"]:
        assert val in pot2
