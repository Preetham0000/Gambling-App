from services.gambler_service import GamblerProfileService
from services.stake_management_service import StakeManagementService
from validation.input_validator import InputValidator
from validation.validation_config import ValidationConfig
from ui.simple_game_engine import SimpleGameEngine


def display_player_setup_menu():
    """Display Player Setup menu"""
    print("\n" + "="*60)
    print("                    PLAYER SETUP")
    print("="*60)
    print("1. Create a new player profile")
    print("2. Load an existing profile")
    print("0. Exit")
    print("="*60)
    
    try:
        choice = int(input("Choose an option [1/2/0] (1): "))
        return choice if choice in [0, 1, 2] else 1
    except ValueError:
        return 1


def create_gambler_profile_enhanced(gambler_service, validator):
    """Enhanced gambler profile creation"""
    print("\n" + "="*60)
    print("          CREATE GAMBLER PROFILE")
    print("="*60)
    
    # Basic Info
    username = input("Choose a username: ").strip()
    full_name = input("Your full name: ").strip()
    email = input("Email address: ").strip()
    
    # Stake Configuration
    while True:
        try:
            initial_stake = float(input("Starting stake: "))
            stake_validation = validator.validate_initial_stake(initial_stake)
            if not stake_validation.is_valid():
                print(stake_validation.summary())
                continue
            break
        except ValueError:
            print("Invalid amount. Please enter a valid number.")
    
    # Win/Loss Thresholds
    while True:
        try:
            win_threshold = float(input(f"Profit target (auto-end when reached) ({initial_stake + 200:.2f}): "))
            loss_threshold = float(input(f"Stop-loss amount ({initial_stake * 0.5:.2f}): "))
            
            limit_validation = validator.validate_limits(loss_threshold, win_threshold, initial_stake)
            if not limit_validation.is_valid():
                print(limit_validation.summary())
                continue
            break
        except ValueError:
            print("Invalid amount. Please enter a valid number.")
    
    # Betting Limits
    while True:
        try:
            min_bet = float(input("Minimum bet amount: "))
            max_bet = float(input("Maximum bet amount: "))
            
            if min_bet <= 0 or max_bet <= 0:
                print("Bet amounts must be positive.")
                continue
            if min_bet >= max_bet:
                print("Minimum bet must be less than maximum bet.")
                continue
            if max_bet > initial_stake:
                print(f"Maximum bet cannot exceed starting stake (₹{initial_stake}).")
                continue
            break
        except ValueError:
            print("Invalid amount. Please enter valid numbers.")
    
    # AutoPlay Mode
    while True:
        autoplay_input = input("Enable auto-play mode? [y/n] (n): ").strip().lower()
        if autoplay_input in ['y', 'n', '']:
            enable_autoplay = autoplay_input == 'y'
            break
        print("Please enter 'y' or 'n'.")
    
    # AutoPlay Limit
    autoplay_limit = 100
    if enable_autoplay:
        while True:
            try:
                autoplay_limit = int(input(f"Auto-play game limit ({autoplay_limit}): ") or "100")
                if autoplay_limit > 0:
                    break
                print("Auto-play limit must be positive.")
            except ValueError:
                print("Invalid number.")
    
    # Create gambler
    gambler_id = gambler_service.create_gambler(
        full_name, email, initial_stake, win_threshold, loss_threshold
    )
    
    return {
        'gambler_id': gambler_id,
        'username': username,
        'full_name': full_name,
        'email': email,
        'initial_stake': initial_stake,
        'win_threshold': win_threshold,
        'loss_threshold': loss_threshold,
        'min_bet': min_bet,
        'max_bet': max_bet,
        'enable_autoplay': enable_autoplay,
        'autoplay_limit': autoplay_limit
    }


def display_gambler_info(gambler_data):
    """Display gambler profile info"""
    print("\n" + "="*60)
    print("                  GAMBLER PROFILE")
    print("="*60)
    print(f"Player ID:          {gambler_data['gambler_id']}")
    print(f"Username:           {gambler_data['username']}")
    print(f"Name:               {gambler_data['full_name']}")
    print(f"Email:              {gambler_data['email']}")
    print(f"Initial Stake:      ₹{gambler_data['initial_stake']:,.2f}")
    print(f"Win Threshold:      ₹{gambler_data['win_threshold']:,.2f}")
    print(f"Loss Threshold:     ₹{gambler_data['loss_threshold']:,.2f}")
    print(f"Min Bet:            ₹{gambler_data['min_bet']:,.2f}")
    print(f"Max Bet:            ₹{gambler_data['max_bet']:,.2f}")
    print(f"AutoPlay Enabled:   {'Yes' if gambler_data['enable_autoplay'] else 'No'}")
    print("="*60)


def display_session_setup_menu():
    """Display Session Setup menu"""
    print("\n" + "="*60)
    print("                    SESSION SETUP")
    print("="*60)
    print("1. Start a new session")
    print("2. Continue an existing session")
    print("0. Exit")
    print("="*60)
    
    try:
        choice = int(input("Choose an option [1/2/0] (1): "))
        return choice if choice in [0, 1, 2] else 1
    except ValueError:
        return 1


def load_gambler_profile(gambler_service):
    """Load an existing gambler profile"""
    print("\n==== LOAD GAMBLER PROFILE ====")
    
    try:
        gambler_id = int(input("Enter gambler ID: "))
        gambler = gambler_service.get_gambler(gambler_id)
        if gambler:
            print(f" Gambler profile loaded successfully!")
            return {
                'gambler_id': gambler_id,
                'username': 'Unknown',
                'full_name': gambler[1] if gambler else 'Unknown',
                'email': gambler[2] if gambler else 'Unknown',
                'initial_stake': gambler[4] if gambler else 0,
                'win_threshold': gambler[6] if gambler else 0,
                'loss_threshold': gambler[7] if gambler else 0,
                'min_bet': 50,
                'max_bet': 500,
                'enable_autoplay': False,
                'autoplay_limit': 100
            }
        else:
            print("✗ Gambler not found!")
            return None
    except ValueError:
        print("Invalid ID. Please enter a valid number.")
        return None


if __name__ == "__main__":

    gambler_service = GamblerProfileService()
    stake_service = StakeManagementService()
    validator = InputValidator(ValidationConfig())

    gambler_data = None

    # Player Setup Phase
    while True:
        choice = display_player_setup_menu()
        
        if choice == 1:
            # Create new player profile
            gambler_data = create_gambler_profile_enhanced(gambler_service, validator)
            if gambler_data:
                display_gambler_info(gambler_data)
                break
        elif choice == 2:
            # Load existing player profile
            gambler_data = load_gambler_profile(gambler_service)
            if gambler_data:
                display_gambler_info(gambler_data)
                break
        else:
            # Exit
            print("Exiting...")
            exit()

    # Session Setup Phase
    while True:
        choice = display_session_setup_menu()
        
        if choice == 1:
            # Start new session
            print(" Starting new session...")
            break
        elif choice == 2:
            # Continue existing session
            print(" Continuing existing session...")
            break
        else:
            # Exit
            print("Exiting...")
            exit()

    # Initialize session
    gambler_id = gambler_data['gambler_id']
    stake_service.initialize_stake(gambler_id, gambler_data['initial_stake'])

    # Start game engine
    engine = SimpleGameEngine(gambler_id, stake_service)
    engine.run()

    print(gambler_service.get_statistics(gambler_id))
    print(gambler_service.validate_gambler(gambler_id))