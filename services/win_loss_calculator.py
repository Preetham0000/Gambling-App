from app.models.game_result import GameResult
from app.models.running_totals import RunningTotals
from app.models.win_loss_statistics import WinLossStatistics
from app.strategies.random_outcome_strategy import RandomOutcomeStrategy


class WinLossCalculator:

    def __init__(self, outcome_strategy=None):
        self.strategy = outcome_strategy or RandomOutcomeStrategy()
        self.totals = RunningTotals()
        self.stats = WinLossStatistics()

    def play(self, bet_amount, stake, probability, odds_config):
        outcome = self.strategy.determine(probability)

        result = GameResult(
            bet_amount,
            outcome,
            stake,
            odds_config,
            probability
        )

        self.totals.update(result)
        self.stats.update(result)

        return result

    def get_summary(self):
        return {
            "totals": {
                "profit": self.totals.net_profit,
                "wins": self.totals.total_wins,
                "losses": self.totals.total_losses
            },
            "stats": self.stats.summary()
        }