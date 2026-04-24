from config.db_config import get_connection


class StakeManagementService:
    """
    Simple stake validation and management service.
    Validates stakes are within acceptable bounds.
    """

    # Stake boundaries
    MIN_STAKE = 100.0
    MAX_STAKE = 1000000.0

    def __init__(self):
        """Initialize stake management service"""
        pass

    def validate_stake(self, amount):
        """
        Validate if stake amount is within acceptable bounds.
        Returns: True if valid, False otherwise
        """
        return self.MIN_STAKE <= amount <= self.MAX_STAKE

    def initialize_stake(self, gambler_id, amount):
        """
        Initialize gambler's stake.
        Validates amount is within bounds.
        """
        if not self.validate_stake(amount):
            raise Exception(
                f"Invalid stake. Must be between {self.MIN_STAKE} and {self.MAX_STAKE}"
            )

        # Update gambler's current_stake in database
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE gambler_profile SET current_stake=%s WHERE id=%s",
            (amount, gambler_id)
        )

        conn.commit()
        cursor.close()
        conn.close()

    def process_bet_result(self, gambler_id, amount, won):
        """
        Process bet result and update gambler's stake.
        Returns: New stake amount
        """
        conn = get_connection()
        cursor = conn.cursor()

        # Get current stake
        cursor.execute(
            "SELECT current_stake FROM gambler_profile WHERE id=%s",
            (gambler_id,)
        )
        result = cursor.fetchone()
        
        if not result:
            raise Exception(f"Gambler {gambler_id} not found")
        
        current_stake = result[0]

        # Calculate new stake
        if won:
            new_stake = current_stake + amount
        else:
            new_stake = current_stake - amount

        # Update database
        cursor.execute(
            "UPDATE gambler_profile SET current_stake=%s WHERE id=%s",
            (new_stake, gambler_id)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return new_stake


        cursor.execute("UPDATE gambler_profile SET current_stake=%s WHERE id=%s", (stake, gambler_id))

        self.repo.insert_transaction(cursor, (
            gambler_id,
            t_type,
            amount,
            stake,
            "BET123"
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return self.boundary.warning(stake)

    # DEPOSIT
    def deposit(self, gambler_id, amount):
        return self._adjust(gambler_id, amount, TransactionType.DEPOSIT)

    # WITHDRAW
    def withdraw(self, gambler_id, amount):
        return self._adjust(gambler_id, -amount, TransactionType.WITHDRAWAL)

    def _adjust(self, gambler_id, amount, t_type):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT current_stake FROM gambler_profile WHERE id=%s", (gambler_id,))
        stake = cursor.fetchone()[0]

        stake += amount

        cursor.execute("UPDATE gambler_profile SET current_stake=%s WHERE id=%s", (stake, gambler_id))

        self.repo.insert_transaction(cursor, (
            gambler_id,
            t_type.value,
            abs(amount),
            stake,
            None
        ))

        conn.commit()
        cursor.close()
        conn.close()

    # MONITOR
    def monitor(self, gambler_id):
        conn = get_connection()
        cursor = conn.cursor()

        rows = self.repo.get_transactions(cursor, gambler_id)

        balances = [r[4] for r in rows]

        peak = max(balances) if balances else 0
        low = min(balances) if balances else 0
        volatility = peak - low

        cursor.close()
        conn.close()

        return {
            "peak": peak,
            "lowest": low,
            "volatility": volatility
        }

    # REPORT
    def report(self, gambler_id):
        conn = get_connection()
        cursor = conn.cursor()

        rows = self.repo.get_transactions(cursor, gambler_id)

        total = len(rows)
        wins = sum(1 for r in rows if r[2] == "BET_WIN")
        losses = sum(1 for r in rows if r[2] == "BET_LOSS")

        cursor.close()
        conn.close()

        return {
            "total_transactions": total,
            "wins": wins,
            "losses": losses,
            "history": rows
        }

    def get_current_stake(self, gambler_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT balance_after
            FROM stake_transaction
            WHERE gambler_id = %s
            ORDER BY id DESC
            LIMIT 1
        """, (gambler_id,))

        row = cursor.fetchone()

        conn.close()

        return row[0] if row else 0


    def update_stake(self, gambler_id, new_stake):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO stake_transaction
            (gambler_id, transaction_type, amount, balance_after)
            VALUES (%s, %s, %s, %s)
        """, (gambler_id, "ADJUSTMENT", 0, new_stake))

        conn.commit()
        conn.close()