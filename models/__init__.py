"""
Models Package - Minimal essential dataclass models for Gambling App
"""

# Import essential models
from models.models import (
    GamblerStatistics,
    BetRecord,
    GameResultRecord,
    WinLossStatistics,
)

# Import Odds Configuration
from models.odds_config import (
    OddsType,
    OddsConfig,
)

__all__ = [
    "GamblerStatistics",
    "BetRecord",
    "GameResultRecord",
    "WinLossStatistics",
    "OddsType",
    "OddsConfig",
]
