class Player:

    def __init__(self):
        self.symbol = None
        self.is_computer = False
        self.opponent_symbol = None

    def opponent_choice(self, player_symbol):           
        self.opponent_symbol = "O" if player_symbol == "X" else "X"
        return self.opponent_symbol

    def computer_or_not(self): 
        return self.is_computer
    
    def computer_move(self, grid):
        import random
        empty_cells = [(r, c) for r in range(len(grid)) for c in range(len(grid[r])) if grid[r][c] is None]
        return random.choice(empty_cells) if empty_cells else None

    def reset_player(self):
        self.symbol = None
        self.is_computer = False
        self.opponent_symbol = None



