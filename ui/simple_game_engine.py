from ui.game_status_display import GameStatusDisplay
from ui.interactive_menu import InteractiveMenu
from ui.session_summary import SessionSummary

from services.win_loss_calculator import WinLossCalculator
from models.odds_config import OddsConfig, OddsType
from validation.input_validator import InputValidator
from validation.validation_config import ValidationConfig


class SimpleGameEngine:

    def __init__(self, gambler_id, stake_service):

        self.gambler_id = gambler_id
        self.stake_service = stake_service

        self.display = GameStatusDisplay()
        self.menu = InteractiveMenu()
        self.summary = SessionSummary()

        self.calculator = WinLossCalculator()
        self.validator = InputValidator(ValidationConfig())

        self.odds = OddsConfig(OddsType.FIXED, 2)
        self.current_game_type = "Heads/Tails"
        self.current_probability = 0.5

    def get_game_config(self, game_type):
        """Get game configuration based on game type"""
        config = {
            1: {
                "name": "STANDARD",
                "description": "Manual Betting - 50/50 Coin Flip - 2x Payout"
            },
            2: {
                "name": "AUTO PLAY",
                "description": "Automatic Betting - 50/50 Coin Flip - 2x Payout"
            }
        }
        return config.get(game_type, config[1])

    def display_bet_confirmation(self, bet_amount, stake, odds, probability, game_type):
        """Display bet details and ask for confirmation"""
        if odds.odds_type == OddsType.FIXED:
            potential_win = bet_amount * odds.value
        else:
            potential_win = bet_amount / probability if probability else bet_amount * 2

        print("\n" + "="*60)
        print("                  CONFIRM BET")
        print("="*60)
        print(f"Game Type:           {game_type}")
        print(f"Current Stake:       ₹{stake:,.2f}")
        print("-"*60)
        print(f"Bet Amount:          ₹{bet_amount:,.2f}")
        print(f"Win Probability:     {probability*100:.1f}%")
        print(f"Odds:                {odds.value}x")
        print("-"*60)
        print(f"If WIN:              +₹{potential_win:,.2f}")
        print(f"If LOSS:             -₹{bet_amount:,.2f}")
        print("-"*60)
        print(f"Potential Stake:     ₹{stake + potential_win:,.2f} (WIN)")
        print(f"Potential Stake:     ₹{stake - bet_amount:,.2f} (LOSS)")
        print("="*60)

    def run(self):

        while True:

            self.menu.display_main_menu()
            choice = self.menu.get_choice()

            if choice == 1:
                self.display.display_current_status(
                    self.gambler_id,
                    self.stake_service
                )

            elif choice == 2:
                self.handle_single_bet()

            elif choice == 3:
                self.handle_multiple_bets()

            elif choice == 4:
                self.summary.display_session_summary(self.calculator)

            elif choice == 5:
                print("Exiting...")
                break

            else:
                print("Invalid choice")

    def handle_single_bet(self):
        """Handle single bet with game type selection and confirmation"""
        
        # Step 1: Choose game type
        game_choice = self.menu.choose_game_type()
        
        if game_choice == 0:
            print("Cancelled.")
            return
        elif game_choice not in [1, 2]:
            print("Invalid choice.")
            return

        # Get game configuration
        game_config = self.get_game_config(game_choice)
        self.current_game_type = game_config['name']
        
        # Set fixed odds and probability for both game types
        self.odds = OddsConfig(OddsType.FIXED, 2)
        self.current_probability = 0.5

        # Step 2: Handle AUTO PLAY differently
        if game_choice == 2:  # AUTO PLAY
            self.handle_autoplay_bets()
            return

        # Step 3: Prompt for bet amount (for STANDARD)
        bet = self.menu.prompt_bet_amount()

        if bet is None:
            print("Invalid input")
            return

        stake = self.stake_service.get_current_stake(self.gambler_id)

        # Step 4: Validate bet
        validation = self.validator.validate_bet_amount(bet, stake)

        if not validation.is_valid():
            print(validation.summary())
            return

        # Step 5: Show bet confirmation with details
        self.display_bet_confirmation(
            bet, 
            stake, 
            self.odds, 
            self.current_probability,
            self.current_game_type
        )

        # Step 6: Get confirmation
        if not self.menu.confirm_bet():
            print("✗ Bet cancelled.")
            return

        # Step 7: Execute bet
        print("\n⟳ Processing bet...")
        import time
        time.sleep(0.5)  # Brief suspense effect

        result = self.calculator.play(
            bet,
            stake,
            self.current_probability,
            self.odds
        )

        self.stake_service.update_stake(self.gambler_id, result.stake_after)

        # Step 8: Display result
        self.display.display_game_outcome(result)

    def handle_autoplay_bets(self):
        """Handle automatic bet playing"""
        print("\n" + "="*60)
        print("                    AUTO PLAY MODE")
        print("="*60)
        
        # Get bet amount
        bet = self.menu.prompt_bet_amount()
        
        if bet is None:
            print("Invalid input")
            return
        
        stake = self.stake_service.get_current_stake(self.gambler_id)
        
        # Validate bet
        validation = self.validator.validate_bet_amount(bet, stake)
        
        if not validation.is_valid():
            print(validation.summary())
            return
        
        # Get number of auto-play games
        while True:
            try:
                num_games = int(input("How many games to play? [default: 5]: ") or "5")
                if num_games > 0:
                    break
                print("Enter a positive number.")
            except ValueError:
                print("Invalid number.")
        
        print(f"\n⟳ Playing {num_games} automatic games with ₹{bet} bet each...\n")
        import time
        time.sleep(1)
        
        for game_num in range(1, num_games + 1):
            print(f"--- Game {game_num}/{num_games} ---")
            
            stake = self.stake_service.get_current_stake(self.gambler_id)
            
            # Check if bet is still valid
            if bet > stake:
                print(f"✗ Insufficient stake. Stopping auto-play.")
                break
            
            result = self.calculator.play(
                bet,
                stake,
                self.current_probability,
                self.odds
            )
            
            self.stake_service.update_stake(self.gambler_id, result.stake_after)
            
            print(f"Outcome: {result.outcome} | Stake: ₹{result.stake_after:,.2f}")
            time.sleep(0.3)
        
        print("\n Auto-play completed!")

    def handle_multiple_bets(self):

        for _ in range(5):
            self.handle_single_bet()