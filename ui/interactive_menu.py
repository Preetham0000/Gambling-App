class InteractiveMenu:

    def display_main_menu(self):
        print("\n==== MAIN MENU ====")
        print("1. Show Status")
        print("2. Place Bet")
        print("3. Play Multiple Bets")
        print("4. Show Summary")
        print("5. Exit")

    def get_choice(self):
        try:
            return int(input("Enter choice: "))
        except:
            return -1

    def prompt_bet_amount(self):
        try:
            return float(input("Enter bet amount: "))
        except:
            return None

    def display_game_types(self):
        """Display available game types"""
        print("\n" + "="*50)
        print("           SELECT GAME TYPE")
        print("="*50)
        print("1. STANDARD       - Manual Betting")
        print("2. AUTO PLAY      - Automatic Betting")
        print("0. Back to Menu")
        print("="*50)
        
    def choose_game_type(self):
        """Get game type choice from user"""
        self.display_game_types()
        try:
            return int(input("Choose game type [0-2]: "))
        except:
            return -1

    def confirm_bet(self):
        """Get bet confirmation from user"""
        try:
            confirmation = input("Confirm bet? [y/n]: ").strip().lower()
            return confirmation == 'y'
        except:
            return False