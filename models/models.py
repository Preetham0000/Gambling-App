"""
Minimal Models for Gambling App
Only essential dataclasses needed for the application
"""
from dataclasses import dataclass, field
from typing import Optional, List


# ============ GAMBLER MODEL ============

@dataclass
class GamblerStatistics:
    """Complete gambler profile and statistics"""
    gambler_id: int
    full_name: str
    email: str
    current_stake: float
    initial_stake: float
    win_threshold: float
    loss_threshold: float
    total_bets: int = 0
    total_wins: int = 0
    total_losses: int = 0
    total_winnings: float = 0.0
    net_profit_loss: float = 0.0
    win_rate: float = 0.0
    account_status: str = "ACTIVE"


# ============ BET MODEL ============

@dataclass
class BetRecord:
    """Individual bet record"""
    bet_id: int
    gambler_id: int
    bet_amount: float
    win_probability: float
    odds_multiplier: float
    outcome: str  # "WIN", "LOSS"
    payout_amount: float
    stake_before: float
    stake_after: float
    placed_at: str


# ============ GAME RESULT MODEL ============

@dataclass
class GameResultRecord:
    """Result of a single game"""
    bet_id: int
    gambler_id: int
    outcome: str  # "WIN", "LOSS"
    payout_amount: float
    net_change: float
    stake_before: float
    stake_after: float
    win_probability: float
    created_at: str


# ============ STATISTICS MODEL ============

@dataclass
class WinLossStatistics:
    """Win/Loss statistics and analytics"""
    total_games: int = 0
    wins: int = 0
    losses: int = 0
    win_rate: float = 0.0
    loss_rate: float = 0.0
    total_winnings: float = 0.0
    total_losses_amount: float = 0.0
    net_profit_loss: float = 0.0
    average_win: float = 0.0
    average_loss: float = 0.0
    largest_win: float = 0.0
    largest_loss: float = 0.0
    current_win_streak: int = 0
    current_loss_streak: int = 0
    longest_win_streak: int = 0
    longest_loss_streak: int = 0
    profit_factor: float = 0.0
    
    def update(self, result):
        """Update statistics with new game result"""
        self.total_games += 1
        
        if result.outcome == "WIN":
            self.wins += 1
            self.total_winnings += result.payout_amount
            self.current_win_streak += 1
            self.current_loss_streak = 0
            if self.current_win_streak > self.longest_win_streak:
                self.longest_win_streak = self.current_win_streak
            if self.largest_win < result.payout_amount:
                self.largest_win = result.payout_amount
        else:
            self.losses += 1
            self.total_losses_amount += result.stake_before - result.stake_after
            self.current_loss_streak += 1
            self.current_win_streak = 0
            if self.current_loss_streak > self.longest_loss_streak:
                self.longest_loss_streak = self.current_loss_streak
            loss_amt = result.stake_before - result.stake_after
            if self.largest_loss < loss_amt:
                self.largest_loss = loss_amt
        
        # Calculate rates
        self.win_rate = (self.wins / self.total_games * 100) if self.total_games > 0 else 0
        self.loss_rate = (self.losses / self.total_games * 100) if self.total_games > 0 else 0
        self.average_win = (self.total_winnings / self.wins) if self.wins > 0 else 0
        self.average_loss = (self.total_losses_amount / self.losses) if self.losses > 0 else 0
        self.net_profit_loss = self.total_winnings - self.total_losses_amount
        self.profit_factor = (self.total_winnings / self.total_losses_amount) if self.total_losses_amount > 0 else 0
    
    def summary(self):
        """Return summary dict"""
        return {
            "total_games": self.total_games,
            "wins": self.wins,
            "losses": self.losses,
            "win_rate": self.win_rate,
            "loss_rate": self.loss_rate,
            "total_winnings": self.total_winnings,
            "total_losses": self.total_losses_amount,
            "net_profit": self.net_profit_loss,
            "average_win": self.average_win,
            "average_loss": self.average_loss,
            "largest_win": self.largest_win,
            "largest_loss": self.largest_loss,
            "max_win_streak": self.longest_win_streak,
            "max_loss_streak": self.longest_loss_streak,
            "profit_factor": self.profit_factor
        }
