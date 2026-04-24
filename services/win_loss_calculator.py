from models import GameResultRecord, WinLossStatistics
from strategies.random_outcome_strategy import RandomOutcomeStrategy


class WinLossCalculator:

    def __init__(self, strategy=None):
        self.strategy = strategy or RandomOutcomeStrategy()
        self.stats = WinLossStatistics()

    def play(self, bet, stake, probability, odds):

        outcome = self.strategy.determine(probability)

        # Calculate payout
        if outcome == "WIN":
            payout = odds.payout(bet, probability)
            stake_after = stake + payout
        else:
            payout = 0
            stake_after = stake - bet

        result = GameResultRecord(
            bet_id=0,  # Will be set by database
            gambler_id=0,  # Will be set by context
            outcome=outcome,
            payout_amount=payout,
            net_change=stake_after - stake,
            stake_before=stake,
            stake_after=stake_after,
            win_probability=probability,
            created_at=""
        )

        self.stats.update(result)

        return result

    def summary(self):
        return self.stats.summary()