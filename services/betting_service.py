import random
from config.db_config import get_connection
from models import BetRecord


class BettingService:
    """Legacy betting service - not currently used"""

    def place_bet(self, gambler_id, amount, probability):
        """Place a single bet (legacy implementation)"""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT current_stake FROM gambler_profile WHERE id=%s",
            (gambler_id,)
        )
        stake = cursor.fetchone()[0]

        if amount > stake:
            raise Exception("Insufficient stake")

        outcome = self._determine_outcome(probability)

        bet = BetRecord(
            bet_id=0,
            gambler_id=gambler_id,
            bet_amount=amount,
            win_probability=probability,
            odds_multiplier=2,
            outcome=outcome,
            payout_amount=amount * 2 if outcome == "WIN" else 0,
            stake_before=stake,
            stake_after=stake + (amount * 2) if outcome == "WIN" else stake - amount,
            placed_at=""
        )

        cursor.close()
        conn.close()

        return bet

    def _determine_outcome(self, probability):
        """Determine bet outcome based on probability"""
        return "WIN" if random.random() < probability else "LOSS"


        if outcome:
            win_amount = bet.calculate_win_amount()
            stake += win_amount
            bet.outcome = "WIN"
        else:
            stake -= amount
            bet.outcome = "LOSS"

        bet.stake_after = stake

        cursor.execute("""
            UPDATE gambler_profile SET current_stake=%s WHERE id=%s
        """, (stake, gambler_id))

        cursor.execute("""
            INSERT INTO bet (gambler_id, amount, win_probability, outcome, stake_before, stake_after)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            gambler_id, amount, probability, bet.outcome,
            bet.stake_before, bet.stake_after
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return bet.outcome

    # RANDOM OUTCOME
    def _determine_outcome(self, probability):
        return random.random() < probability

    # STRATEGY BET
    def place_bet_with_strategy(self, gambler_id, strategy, context, probability):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT current_stake FROM gambler_profile WHERE id=%s", (gambler_id,))
        stake = cursor.fetchone()[0]

        amount = strategy.get_bet_amount(stake, context)

        outcome = self.place_bet(gambler_id, amount, probability)

        context["last_outcome"] = outcome
        context["last_bet"] = amount

        return outcome

    # MULTIPLE BETS
    def place_consecutive_bets(self, gambler_id, strategy, rounds, probability):
        context = {}
        results = []

        for _ in range(rounds):
            result = self.place_bet_with_strategy(gambler_id, strategy, context, probability)
            results.append(result)

        return results