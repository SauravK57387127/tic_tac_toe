import pygame
from tic_tac_toe.board import BoardManager
from tic_tac_toe.player import Player





class Game:
    def __init__(self):
        self.player = Player()
        self.board_manager = BoardManager()

        self.choose_symbol_state = ChooseSymbolState(self)
        self.choose_opponent_state = ChooseOpponentState(self)
        self.board_state = BoardState(self)
        self.game_over_state = GameOverState(self)

        self.current_state = self.choose_symbol_state

        self.board_manager.initialize_window()
        self.screen = self.board_manager.get_screen()

        self.player_turn = True


    def handle_turns(self, cell_clicked):
        row, col = cell_clicked
        result = None

        # Player's turn
        if self.player_turn:
            if self.board_manager.grid.grid[row][col] is None:
                self.board_manager.update_cell(cell_clicked, self.player.symbol)
                result = self.board_manager.grid.check_win(row, col, self.player.symbol)
                
                if result:
                    return result
                
                self.player_turn = not self.player_turn  # Toggle turn


        # Opponent's turn (Human)
        elif not self.player.is_computer:
            if self.board_manager.grid.grid[row][col] is None:
                self.board_manager.update_cell(cell_clicked, self.player.opponent_symbol)
                result = self.board_manager.grid.check_win(row, col, self.player.opponent_symbol)
                if result:
                    return result

                self.player_turn = not self.player_turn  # Toggle turn
    

        # Computer's turn
        elif self.player.is_computer:
            computer_move = self._computer_clicked_cell()
            self.board_manager.update_cell(computer_move, self.player.opponent_symbol)
            result = self.board_manager.grid.check_win(computer_move[0], computer_move[1], self.player.opponent_symbol)

            if result:
                return result
            
            self.player_turn = not self.player_turn  # Toggle turn


        return result
    

    def _computer_clicked_cell(self):
        computer_move = self.player.computer_move(self.board_manager.grid.grid)
        return computer_move
    

    def set_state(self, new_state):
        """Change the current state of the game."""
        # print(f"Transitioning to {new_state.__class__.__name__}")
        self.current_state = new_state

    def handle_event(self, event):
        """Delegate event handling to the current state."""
        # print(f"\n{self.__class__.__name__} received event: {event}")
        self.current_state.handle_events(event)

    def render(self):
        """Delegate rendering to the current state."""
        self.current_state.render_state(self.screen)




class GameState:
    def __init__(self, game, game_over_message="GAME OVER"):
        self.game = game  
        self.game_over_message = game_over_message

    def handle_events(self, event):
        raise NotImplementedError

    def render_state(self):
        raise NotImplementedError



class ChooseSymbolState(GameState):
    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:

            symbol_chosen = self.game.board_manager.capture_symbol_choice(event.pos)

            if symbol_chosen:
                self.game.player.symbol = symbol_chosen
                self.game.opponent_symbol = self.game.player.opponent_choice(symbol_chosen)

                print(f"\nPlayer chose: {symbol_chosen},  Opponent Gets: {self.game.opponent_symbol}")

                self.game.set_state(ChooseOpponentState(self.game))


    def render_state(self, screen):
        self.game.board_manager.render_specific_state("choose_symbol")




class ChooseOpponentState(GameState):
    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:

            opponent_chosen = self.game.board_manager.capture_opponent_choice(event.pos)

            if opponent_chosen:
                self.game.player.is_computer = True if opponent_chosen.upper() == "C" else False

                if self.game.player.is_computer:
                    print(f"\nPlaying against  COMPUTER  and its symbol is: {self.game.opponent_symbol}")
                else:
                    print(f"\nPlaying against  HUMAN  and his symbol is: {self.game.opponent_symbol}")
                
                self.game.set_state(BoardState(self.game))


    def render_state(self, screen):
        self.game.board_manager.render_specific_state("choose_opponent")




class BoardState(GameState):

    def handle_events(self, event):
        # Handle player's turn
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked_at = event.pos

            for (row, col), cell in self.game.board_manager.grid.cells:
                if cell.collidepoint(clicked_at):

                    result = self.game.handle_turns((row, col))

                    if result:
                        self.game_over_message = result   
                        self.game.set_state(GameOverState(self.game, self.game_over_message))
                        return


        # Handle computer's turn immediately after the player's move
        if not self.game.player_turn and self.game.player.is_computer:
            result = self.game.handle_turns(self.game._computer_clicked_cell())

            if result:
                self.game_over_message = result
                self.game.set_state(GameOverState(self.game, self.game_over_message))
                return
        

    def render_state(self, screen):
        self.game.board_manager.render_specific_state("board")




class GameOverState(GameState):
    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            restart_game = self.game.board_manager.restart_clicked(event)
            if restart_game:
                self.game.board_manager.reset_board()
                self.game.player.reset_player()
                self.game.player_turn = True
                self.game.set_state(ChooseSymbolState(self.game))


    def render_state(self, screen):
        self.game.board_manager.render_specific_state("game_over", self.game_over_message)

















'''OLD Version'''




# class Game:
#     def __init__(self, player, board):
#         self.player = player
#         self.board = board



#     def run(self):
#         running = True
#         while running:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     running = False

#                 cell_clicked = self.board.handle_events(event)

#                 if cell_clicked:
#                     row, col = cell_clicked

#                     if self.board.grid[row][col] is None:

#                         current_symbol = self.board.player_symbol if self.is_player_turn else self.board.opponent_symbol
#                         self.board.grid[row][col] = current_symbol

#                         self.board.draw_symbol(cell_clicked, current_symbol)
#                         self.board.update_grid(cell_clicked, current_symbol)

#                         print(self.board.grid)

#                         winner = self.who_won(row, col, current_symbol)
#                         if winner:
#                             continue
#                         else:
#                             self.is_player_turn = not self.is_player_turn

#             if not self.is_player_turn and self.board.opponent == "C":
#                 c_row, c_col = self.computer_move()

#                 self.board.draw_symbol((c_row, c_col), self.board.opponent_symbol)
#                 self.board.update_grid((c_row, c_col), self.board.opponent_symbol)

#                 winner = self.who_won(c_row, c_col, self.board.opponent_symbol)

#                 if winner:
#                     continue
#                 else:
#                     self.is_player_turn = True

#             self.board.render_state()
#             pygame.display.update()


#     def who_won(self, row, col, player_symbol):
#         winner = self.board.check_win(row, col, player_symbol)

#         if winner:
#             self.board.state = "game_over"
#             self.board.winner_message = winner
#             return True  
        
#         return False







        


    
    
