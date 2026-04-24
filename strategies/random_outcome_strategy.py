import random
from app.strategies.outcome_base import OutcomeStrategy

class RandomOutcomeStrategy(OutcomeStrategy):
    def determine(self, probability):
        return "WIN" if random.random() < probability else "LOSS"