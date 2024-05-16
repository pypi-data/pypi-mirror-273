"""Test pruning parts."""
import igraph as ig
import pandas as pd
from scicom.historicalletters.model import (
    HistoricalLetters,
)
from scicom.utilities.statistics import (
    PruneNetwork,
)

#####
# Test pruning setup
#####


def test_pruning() -> None:
    """Model initialization puts agents on sheduler."""
    model = HistoricalLetters(
        population=30,
    )
    model.run(20)
    columns = ["sender", "receiver", "sender_location", "receiver_location", "topic", "step"]
    network = pd.DataFrame(model.letterLedger, columns = columns)
    pruning = PruneNetwork(dataframe=network)

    graph = pruning.makeNet(dataframe=network)

    assert isinstance(graph, ig.Graph)

    dataagents = pruning.setSurvivalProb(
        graph=graph, method="agents",
    )

    assert isinstance(dataagents, pd.DataFrame)

    dataregions = pruning.setSurvivalProb(
        graph=graph, method="regions",
    )
    assert isinstance(dataregions, pd.DataFrame)

    datatimesteps = pruning.setSurvivalProb(
        graph=graph, method="time",
    )
    assert isinstance(datatimesteps, pd.DataFrame)


def test_model_initialization_with_pruning() -> None:
    """Model initialization puts agents on sheduler."""
    model = HistoricalLetters(
        population=100,
        runPruning=True,
        debug=True,
    )
    # 100 agents should be on the scheduler
    c1 = 100
    assert len(model.schedule.agents) == c1
    model.run(50)


