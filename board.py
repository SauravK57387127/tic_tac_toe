import pygame




'''Modified Version'''


class _VisualConstants:
    # General Constants
    WINDOW_WIDTH = 500
    WINDOW_HEIGHT = 500
    GRID_SIZE = 300
    CELL_SIZE = 90
    MARGIN = 10
    GRID_X, GRID_Y = (WINDOW_WIDTH - GRID_SIZE) // 2, (WINDOW_HEIGHT - GRID_SIZE) // 2
    
    # Dimensions for Choice Screens
    CHOOSE_OPTION_WIDTH = (CELL_SIZE + MARGIN) * 3
    CHOOSE_OPTION_HEIGHT = (CELL_SIZE + MARGIN)

    # Symbol Choice Box Positions
    SYMBOL_CHOICE_X = GRID_X + (CELL_SIZE + MARGIN) // 2
    SYMBOL_CHOICE_Y = GRID_Y + CHOOSE_OPTION_HEIGHT + MARGIN

    # Opponent Choice Box Positions
    OPPONENT_CHOICE_X = GRID_X + (CELL_SIZE + MARGIN) // 2
    OPPONENT_CHOICE_Y = GRID_Y + CHOOSE_OPTION_HEIGHT + MARGIN

    # Player Information Boxes
    PLAYER_BOX_WIDTH = CELL_SIZE // 2
    PLAYER_BOX_HEIGHT = CELL_SIZE // 2
    PLAYER_BOX_TOP_X = GRID_X - PLAYER_BOX_WIDTH - MARGIN
    PLAYER_BOX_TOP_Y = GRID_Y

    PLAYER_BOX_BOTTOM_X = GRID_X + 2 * (CELL_SIZE + MARGIN) + CELL_SIZE + MARGIN
    PLAYER_BOX_BOTTOM_Y = GRID_Y + 2 * (CELL_SIZE + MARGIN) + PLAYER_BOX_HEIGHT

    # Player Symbol Text Positions
    PLAYER_SYMBOL_TEXT_X = GRID_X - CELL_SIZE // 2
    PLAYER_SYMBOL_TEXT_Y = GRID_Y

    OPPONENT_SYMBOL_TEXT_X = GRID_X + 2 * (CELL_SIZE + MARGIN) + CELL_SIZE + 2 * MARGIN
    OPPONENT_SYMBOL_TEXT_Y = GRID_Y + 2 * (CELL_SIZE + MARGIN) + CELL_SIZE // 2




class Grid:
    def __init__(self, constants: _VisualConstants, grid=None):
        self.constants = constants
        self.grid = grid or [[None] * 3 for _ in range(3)]
        self.cells = []


    def create_game_board_cells(self):
        if not self.cells:
            for row in range(3):
                for col in range(3):

                    CELL_X = self.constants.GRID_X + (self.constants.CELL_SIZE + self.constants.MARGIN) * col
                    CELL_Y = self.constants.GRID_Y + (self.constants.CELL_SIZE + self.constants.MARGIN) * row
                    
                    self.cells.append(( (row, col), pygame.Rect(CELL_X, CELL_Y, self.constants.CELL_SIZE, self.constants.CELL_SIZE)))


    def _update_cell(self, grid_index, symbol=None):
        r, c = grid_index
        self.grid[r][c] = symbol


    def _clear_cell(self, grid_index):
        self.update_cell(grid_index, None)


    def reset_grid(self):
        self.grid = [[None] * 3 for _ in range(3)]


    def check_win(self, row, col, current_player_symbol):

        if all(self.grid[row][i] == current_player_symbol for i in range(3)):
            # print(f"Checking win for: {current_player_symbol} along same ROW")
            return f"{current_player_symbol} Wins!"

        if all(self.grid[i][col] == current_player_symbol for i in range(3)):
            # print(f"Checking win for: {current_player_symbol} along same COL")
            return f"{current_player_symbol} Wins!"

        if row == col and all(self.grid[i][i] == current_player_symbol for i in range(3)):
            # print(f"Checking win for: {current_player_symbol} along diagonal")
            return f"{current_player_symbol} Wins!"

        if row + col == 2 and all(self.grid[i][2 - i] == current_player_symbol for i in range(3)):
            # print(f"Checking win for: {current_player_symbol} other diagonal")
            return f"{current_player_symbol} Wins!"

        if all(self.grid[r][c] is not None for r in range(3) for c in range(3)):
            # print(f"Checking win for: {current_player_symbol}")
            return "It's a Tie!"

        return None
    



class Renderer:

    def __init__(self, constants: _VisualConstants, screen=None):
        self.constants = constants
        self.screen = screen

    def initialize_game_window(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.constants.WINDOW_WIDTH, self.constants.WINDOW_HEIGHT))
        pygame.display.set_caption("TIC TAC TOE")
        self.screen.fill((128, 128, 128))


    def render_background(self, color=(128, 128, 128)):
        self.screen.fill(color)


    def render_game_board(self, grid):
        grid.create_game_board_cells()

        # self.render_player_information_boxes()
        
        for (row, col), rect in grid.cells:
            symbol = grid.grid[row][col]

            pygame.draw.rect(self.screen, (255, 255, 255), rect)
            if symbol:
                self.render_symbol_at_position((row, col), symbol, grid.cells)


    def render_symbol_at_position(self, grid_index, symbol, grid_cells):
        if symbol == "O":
            self._render_symbol_O(grid_index, grid_cells)
        elif symbol == "X":
            self._render_symbol_X(grid_index, grid_cells)


    def _render_symbol_O(self, grid_index, grid_cells):
        for (row, col), rect in grid_cells:
            if (row, col) == grid_index:  
                x, y, w, h = rect.x, rect.y, rect.width, rect.height

                center = (x + w // 2, y + h // 2)    
                radius = w // 2 - 5    

                pygame.draw.circle(self.screen, (0, 0, 0), center, radius, 8)  
                break

    
    def _render_symbol_X(self, grid_index, grid_cells):
        for (row, col), rect in grid_cells:
            if (row, col) == grid_index:  
                x, y, w, h = rect.x, rect.y, rect.width, rect.height

                offset = 10

                pygame.draw.line(self.screen, (0, 0, 0), 
                                (x + offset, y + offset), 
                                (x + w - offset, y + h - offset), 16)  
                pygame.draw.line(self.screen, (0, 0, 0), 
                                (x + w - offset, y + offset), 
                                (x + offset, y + h - offset), 16)  
                break


    def render_player_information_boxes(self):
        pygame.draw.rect(
            self.screen, (255, 255, 255),
            (
                self.constants.PLAYER_BOX_TOP_X, 
                self.constants.PLAYER_BOX_TOP_Y,
                self.constants.PLAYER_BOX_WIDTH,
                self.constants.PLAYER_BOX_HEIGHT
            )
        )
 
        pygame.draw.rect(
            self.screen, (255, 255, 255),
            (
                self.constants.PLAYER_BOX_BOTTOM_X, 
                self.constants.PLAYER_BOX_BOTTOM_Y,
                self.constants.PLAYER_BOX_WIDTH,
                self.constants.PLAYER_BOX_HEIGHT
            )
        )


    def render_player_information_in_boxes(self, player, opponent):
        font = pygame.font.Font(None, 66)  
        text = font.render(opponent, True, (0, 0, 0))    
        self.screen.blit(
            text, 
            (self.constants.PLAYER_SYMBOL_TEXT_X, self.constants.PLAYER_SYMBOL_TEXT_Y)
        )

        text = font.render(player, True, (0, 0, 0))    
        self.screen.blit(
            text, 
            (self.constants.OPPONENT_SYMBOL_TEXT_X, self.constants.OPPONENT_SYMBOL_TEXT_Y)
        )


    def render_symbol_choice_screen(self):        
        self._render_selection_box(
            self.constants.GRID_X, self.constants.GRID_Y, 
            self.constants.CHOOSE_OPTION_WIDTH, 
            self.constants.CHOOSE_OPTION_HEIGHT, 
            (255, 255, 255), "Choose Symbol"
        )

        self._render_selection_box(
            self.constants.SYMBOL_CHOICE_X, self.constants.SYMBOL_CHOICE_Y, 
            self.constants.CHOOSE_OPTION_WIDTH // 3, 
            self.constants.CHOOSE_OPTION_HEIGHT, 
            (255, 255, 255), "O"
        )

        self._render_selection_box(
            self.constants.SYMBOL_CHOICE_X + self.constants.CHOOSE_OPTION_WIDTH // 3 + self.constants.MARGIN, 
            self.constants.SYMBOL_CHOICE_Y, 
            self.constants.CHOOSE_OPTION_WIDTH // 3, 
            self.constants.CHOOSE_OPTION_HEIGHT, 
            (255, 255, 255), "X"
        )
    

    def render_opponent_choice_screen(self):  
        self._render_selection_box(
            self.constants.GRID_X, self.constants.GRID_Y, 
            self.constants.CHOOSE_OPTION_WIDTH, 
            self.constants.CHOOSE_OPTION_HEIGHT, 
            (255, 255, 255), "Choose Opponent"
        )

        self._render_selection_box(
            self.constants.OPPONENT_CHOICE_X, self.constants.OPPONENT_CHOICE_Y, 
            self.constants.CHOOSE_OPTION_WIDTH // 3, 
            self.constants.CHOOSE_OPTION_HEIGHT, 
            (255, 255, 255), "C"
        )

        self._render_selection_box(
            self.constants.OPPONENT_CHOICE_X + self.constants.CHOOSE_OPTION_WIDTH // 3 + self.constants.MARGIN, 
            self.constants.OPPONENT_CHOICE_Y, 
            self.constants.CHOOSE_OPTION_WIDTH // 3, 
            self.constants.CHOOSE_OPTION_HEIGHT, 
            (255, 255, 255), "P"
        )


    def _render_board_with_cleared_state(self, grid):
        for (row, col), cell in grid.cells:
            pygame.draw.rect(self.screen, (255, 255, 255), cell)

            symbol = grid.grid[row][col]
            if symbol:  
                self.render_symbol_at_position((row, col), symbol, grid.cells)


    def render_game_over_screen(self, grid, message):
        self._render_board_with_cleared_state(grid)

        font = pygame.font.Font(None, 50)
        text = font.render(message, True, (255, 0, 0))  
        text_rect = text.get_rect(center=(self.constants.WINDOW_WIDTH // 2, self.constants.WINDOW_WIDTH // 2))
        self.screen.blit(text, text_rect)

        button_font = pygame.font.Font(None, 36)
        button_text = button_font.render("again?", True, (255, 255, 255))
        
        self.restart_rect = pygame.Rect(self.constants.WINDOW_WIDTH // 2 - 60, self.constants.WINDOW_WIDTH // 2 + 30, 110, 60)

        pygame.draw.rect(self.screen, (98, 219, 89), self.restart_rect)
        self.screen.blit(button_text, button_text.get_rect(center=self.restart_rect.center))

        return self.restart_rect
    

    def _render_selection_box(self, grid_x, grid_y, width, height, color, text=None):
        dimensions = (grid_x, grid_y, width, height)
        pygame.draw.rect(self.screen, color, dimensions)

        if text:
            font = pygame.font.Font(None, 46)  
            text_surface = font.render(text, True, (0, 0, 0))  
            text_rect = text_surface.get_rect(center=(grid_x + width // 2, grid_y + height // 2))
            self.screen.blit(text_surface, text_rect)


    def render_clear_cell(self, grid_index, grid_cells):
        for (row, col), rect in grid_cells:
            if (row, col) == grid_index:
                x, y, w, h = rect.x, rect.y, rect.width, rect.height
                pygame.draw.rect(self.screen, (255, 255, 255), (x, y, w, h))
                return True
            
        return False


    def render_clear_all_cells(self, grid_cells):
        for (row, col), rect in grid_cells:
            self.render_clear_cell((row, col), grid_cells)






class BoardManager:
    
    def __init__(self):
        self.constants = _VisualConstants()
        self.grid = Grid(self.constants)
        self.renderer = Renderer(self.constants, None)

        self.symbol_cells = {}
        self.opponent_cells = {}


    '''             Init pygame WINDOW & screen              '''

    def initialize_window(self):
        self.renderer.initialize_game_window()

    def get_screen(self):
        return self.renderer.screen
    
    def background(self):
        return self.renderer.render_background()


    
    '''             GAME OVER &   Restart BUTTON              '''

    def restart_clicked(self, event):
        if self.renderer.restart_rect.collidepoint(event.pos):
            return True
        return False
    


    '''             Init SYMBOL & BOARD CELLS DIMENSIONS                '''

    def _initialize_symbol_cells(self):
        self.symbol_cells = {
            "O": pygame.Rect(
                self.constants.SYMBOL_CHOICE_X, 
                self.constants.SYMBOL_CHOICE_Y, 
                self.constants.CHOOSE_OPTION_WIDTH // 3, 
                self.constants.CHOOSE_OPTION_HEIGHT
            ),
            "X": pygame.Rect(
                self.constants.SYMBOL_CHOICE_X + self.constants.CHOOSE_OPTION_WIDTH // 3 + self.constants.MARGIN, 
                self.constants.SYMBOL_CHOICE_Y, 
                self.constants.CHOOSE_OPTION_WIDTH // 3, 
                self.constants.CHOOSE_OPTION_HEIGHT
            )
        }


    def _initialize_opponent_cells(self):
        self.opponent_cells = {
            "C": pygame.Rect(
                self.constants.OPPONENT_CHOICE_X, 
                self.constants.OPPONENT_CHOICE_Y, 
                self.constants.CHOOSE_OPTION_WIDTH // 3, 
                self.constants.CHOOSE_OPTION_HEIGHT
            ),
            "P": pygame.Rect(
                self.constants.OPPONENT_CHOICE_X + self.constants.CHOOSE_OPTION_WIDTH // 3 + self.constants.MARGIN, 
                self.constants.OPPONENT_CHOICE_Y, 
                self.constants.CHOOSE_OPTION_WIDTH // 3, 
                self.constants.CHOOSE_OPTION_HEIGHT
            )
        }



    '''             CLEAR, UPDATE & RESET             '''    
    def update_cell(self, grid_index, symbol): 
        self.grid._update_cell(grid_index, symbol)

    def clear_cell(self, row, col): 
        self.grid._clear_cell((row, col))
        self.renderer.render_clear_cell((row, col), self.grid.cells)

    def reset_board(self):
        self.renderer.render_clear_all_cells(self.grid.cells)
        self.grid.reset_grid()


    
    '''             CAPTURE SYMBOL AND OPPONENT CLICKED             '''

    def capture_symbol_choice(self, mouse_pos):
        for symbol, rect in self.symbol_cells.items():
            if rect.collidepoint(mouse_pos):
                return symbol
            
        return None

    def capture_opponent_choice(self, mouse_pos):
        for opponent, rect in self.opponent_cells.items():
            if rect.collidepoint(mouse_pos):
                return opponent
            
        return None
    


    '''             RENDERING TASKS             '''

    def render_specific_state(self, state, message=None):
        self.renderer.render_background()

        if state == "choose_symbol":
            self._initialize_symbol_cells()
            self.renderer.render_symbol_choice_screen()

        elif state == "choose_opponent":
            self._initialize_opponent_cells()
            self.renderer.render_opponent_choice_screen()

        elif state == "board":
            self.renderer.render_game_board(self.grid)

        elif state == "game_over":
            self.renderer.render_game_over_screen(self.grid, message)












'''OLD VERSION'''




# from player import Player




# class Board:
#     def __init__(self, grid=None, window_size=500, screen=None, grid_size=300, cell_size=90, margin=10):
#         '''This part is shifted to Grid'''
#         self.grid = grid or [[None]*3 for _ in range(3)]
#         self.cells = []

#         self.player = Player()

#         '''This part is shifted to Renderer!'''
#         self.screen = screen
#         self.window_size = window_size
#         self.grid_size = grid_size
#         self.cell_size = cell_size
#         self.margin = margin

#         '''This is going to be the logic which board manager handles.'''
#         self.player_symbol = None
#         self.opponent = None
#         self.opponent_symbol = None

#         self.state = "choose_symbol"
#         self.winner_message = "game_over"


#     def render_state(self):
#         self.screen.fill((128, 128, 128))  

#         if self.state == "choose_symbol":
#             self.render_choose_symbol()
#         elif self.state == "choose_opponent":
#             self.render_choose_opponent()
#         elif self.state == "board":
#             self.render_board()
#         elif self.state == "game_over":
#             self.render_game_over(self.winner_message)


#     def handle_events(self, event): 
#         if event.type == pygame.MOUSEBUTTONDOWN:

#             if self.state == "choose_symbol":
#                 selected_symbol = self.symbol_chosen(event.pos)
#                 if selected_symbol:
#                     print(f"Player chose: {self.player_symbol}, Opponent gets: {self.opponent_symbol}")
#                     self.state = "choose_opponent"  

#             elif self.state == "choose_opponent":
#                 opponent = self.opponent_chosen(event.pos)
#                 if opponent:
#                     print(f"Playing against {self.opponent} and its symbol is {self.opponent_symbol}")
#                     self.state = "board"  

#             elif self.state == "board": 

#                 clicked_at = event.pos
#                 for index, cell in self.cells:
#                     if cell.collidepoint(clicked_at):

#                         print()
#                         print(f"updated grid: ")
#                         print('\n'.join(str([j for j in row]) for row in self.grid))
#                         print()

#                         return index

#             elif self.state == "game_over": 
#                 if self.restart_rect.collidepoint(event.pos):
#                     self.reset_game()


#     '''Done!'''
#     def render_choose_symbol(self):
#         GRID_X, GRID_Y = (self.window_size - self.grid_size) // 2, (self.window_size - self.grid_size) // 2
#         width = (self.cell_size + self.margin) * 3
#         height = (self.cell_size + self.margin)

#         self.draw_box(GRID_X, GRID_Y, width, height, (255, 255, 255), "Choose Symbol")

#         self.symbol_cells = {
#             "O": pygame.Rect(GRID_X + (self.cell_size + self.margin) // 2, GRID_Y + height + self.margin, width // 3, height),
#             "X": pygame.Rect(GRID_X + (width + self.margin * 2) // 2, GRID_Y + height + self.margin, width // 3, height),
#         }

#         self.draw_box(GRID_X + (self.cell_size + self.margin) // 2, GRID_Y + height + self.margin, width // 3, height, (255, 255, 255), "O")
#         self.draw_box(GRID_X + (width + self.margin * 2) // 2, GRID_Y + height + self.margin, width // 3, height, (255, 255, 255), "X")
    

#     '''Done!'''
#     def render_choose_opponent(self):
#         GRID_X, GRID_Y = (self.window_size - self.grid_size) // 2, (self.window_size - self.grid_size) // 2
#         width = (self.cell_size + self.margin) * 3
#         height = (self.cell_size + self.margin)

#         self.draw_box(GRID_X, GRID_Y, width, height, (255, 255, 255), "Choose Opponent")

#         self.opponent_cells = {
#             "P": pygame.Rect(GRID_X + (self.cell_size + self.margin) // 2, GRID_Y + height + self.margin, width // 3, height),
#             "C": pygame.Rect(GRID_X + (width + self.margin * 2) // 2, GRID_Y + height + self.margin, width // 3, height),
#         }

#         self.draw_box(GRID_X + (self.cell_size + self.margin) // 2, GRID_Y + height + self.margin, width // 3, height, (255, 255, 255), "P")
#         self.draw_box(GRID_X + (width + self.margin * 2) // 2, GRID_Y + height + self.margin, width // 3, height, (255, 255, 255), "C")


#     '''Done!'''
#     def symbol_chosen(self, mouse_pos):
#         for symbol, rect in self.symbol_cells.items():
#             if rect.collidepoint(mouse_pos):
#                 self.player_symbol = symbol
#                 self.opponent_symbol = self.player.opponent_symbol(self.player_symbol)

#                 # print(f"Player chose: {self.player_symbol}, Opponent gets: {self.opponent_symbol}")
#                 return True
            
#         return False
    

#     '''Done!!'''
#     def opponent_chosen(self, mouse_pos):
#         for opponent, rect in self.opponent_cells.items():
#             if rect.collidepoint(mouse_pos): 
#                 self.opponent = opponent
#                 return True
        
#         return False


#     '''DONE !!'''
#     def reset_game(self):
#         self.grid = [[None]*3 for _ in range(3)]  
#         self.cells = []
#         self.cells_initialized = False
#         self.player_symbol = None  
#         self.opponent = None  
#         self.opponent_symbol = None  
#         self.state = "choose_symbol"  
#         self.screen.fill((128, 128, 128))


'''
        Clearing cell rendering is placed in Renderer.
        Updating will be handled in BoardManager.

        Done!!
'''
#     def clear_cell(self, position):
#         for (row, col), rect in self.cells:
#             if (row, col) == position:  
#                 x, y, w, h = rect.x, rect.y, rect.width, rect.height
#                 pygame.draw.rect(self.screen, (255, 255, 255), (x, y, w, h))
#                 break

#         self.update_grid(position, None)


#     '''Shifted to Renderer'''
#     def make_window(self):
#         pygame.init()
#         self.screen = pygame.display.set_mode((self.window_size, self.window_size))
#         pygame.display.set_caption("TIC TAC TOE")
#         self.screen.fill((128, 128, 128))

#     '''Shifted to Renderer'''
#     def render_board(self):
#         if not hasattr(self, 'cells_initialized') or not self.cells_initialized:
#             self.make_cells()
#             self.cells_initialized = True

#         self.display_player_boxes()

#         for (row, col), rect in self.cells:
#             pygame.draw.rect(self.screen, (255, 255, 255), rect)
#             self.draw_symbol((row, col), self.grid[row][col])

#     '''Shifted to renderer'''
#     def render_static_board(self):
#         for index, cell in self.cells:
#             pygame.draw.rect(self.screen, (255, 255, 255), cell)
#             if self.grid[index[0]][index[1]]:  
#                 self.draw_symbol(index, self.grid[index[0]][index[1]])

#     '''Shifted to Renderer'''
#     def draw_symbol(self, index, symbol):
#         if symbol == "O":
#             self.draw_O((index))
#         elif symbol == "X":
#             self.draw_X((index))

#     '''Shifted to Grid'''
#     def make_cells(self):    
#         GRID_X, GRID_Y = (self.window_size - self.grid_size) // 2, (self.window_size - self.grid_size) // 2

#         for row in range(3):
#             for col in range(3):
#                 cell_x = GRID_X + col * (self.cell_size + self.margin)
#                 cell_y = GRID_Y + row * (self.cell_size + self.margin)
#                 self.cells.append(( (row, col), pygame.Rect(cell_x, cell_y, self.cell_size, self.cell_size) ))


#     '''Shifted to Grid class'''
#     def check_win(self, row, col, current_player_symbol):
#         if all(self.grid[row][i] == current_player_symbol for i in range(3)):
#             return f"{current_player_symbol} Wins!"

#         if all(self.grid[i][col] == current_player_symbol for i in range(3)):
#             return f"{current_player_symbol} Wins!"

#         if row == col and all(self.grid[i][i] == current_player_symbol for i in range(3)):
#             return f"{current_player_symbol} Wins!"

#         if row + col == 2 and all(self.grid[i][2 - i] == current_player_symbol for i in range(3)):
#             return f"{current_player_symbol} Wins!"

#         if all(self.grid[r][c] is not None for r in range(3) for c in range(3)):
#             return "It's a Tie!"

#         return None  
    
#     '''Shifted to Renderer'''
#     def draw_box(self, GRID_X, GRID_Y, width, height, color, text=None):
#         dimensions = (GRID_X, GRID_Y, width, height)
#         pygame.draw.rect(self.screen, color, dimensions)

#         if text:
#             font = pygame.font.Font(None, 46)  
#             text_surface = font.render(text, True, (0, 0, 0))  
#             text_rect = text_surface.get_rect(center=(GRID_X + width // 2, GRID_Y + height // 2))
#             self.screen.blit(text_surface, text_rect)

    


#     '''Shifted to Renderer'''
#     def draw_X(self, position):    
#         for (row, col), rect in self.cells:
#             if (row, col) == position:  
#                 x, y, w, h = rect.x, rect.y, rect.width, rect.height

#                 offset = 10

#                 pygame.draw.line(self.screen, (0, 0, 0), 
#                                 (x + offset, y + offset), 
#                                 (x + w - offset, y + h - offset), 16)  
#                 pygame.draw.line(self.screen, (0, 0, 0), 
#                                 (x + w - offset, y + offset), 
#                                 (x + offset, y + h - offset), 16)  
#                 break


#     '''Shifted to Renderer'''
#     def draw_O(self, position):
#         for (row, col), rect in self.cells:
#             if (row, col) == position:  
#                 x, y, w, h = rect.x, rect.y, rect.width, rect.height

#                 center = (x + w // 2, y + h // 2)    
#                 radius = w // 2 - 5    

#                 pygame.draw.circle(self.screen, (0, 0, 0), center, radius, 8)  
#                 break


#     '''Shifted to Grid'''
#     def update_grid(self, position, symbol=None):
#         r, c = position
#         self.grid[r][c] = symbol

#     '''Shifted to Renderer'''
#     def display_player_boxes(self):
#         # Box for Player 1 (Top Left)
#         GRID_X, GRID_Y = (self.window_size - self.grid_size) // 2, (self.window_size - self.grid_size) // 2
#         font = pygame.font.Font(None, 66)  

#         # Box for Player 1 (Top Left)
#         pygame.draw.rect(self.screen, (255, 255, 255), 
#                         (GRID_X - self.cell_size // 2 - self.margin, GRID_Y, self.cell_size // 2, self.cell_size // 2))
        
#         text = font.render(self.opponent, True, (0, 0, 0))  
#         self.screen.blit(text, (GRID_X - (self.cell_size // 2), GRID_Y))

#         # Box for Player 2 (Bottom Left, placed near the last cell)
#         last_cell_x = GRID_X + 2 * (self.cell_size + self.margin) 
#         last_cell_y = GRID_Y + 2 * (self.cell_size + self.margin)  

#         # Place the Player 2 box below the last cell
#         pygame.draw.rect(self.screen, (255, 255, 255), 
#                         (last_cell_x + self.cell_size + self.margin, last_cell_y + self.cell_size // 2, self.cell_size // 2, self.cell_size // 2))  
        
#         text = font.render(self.player.symbol, True, (0, 0, 0))  
#         self.screen.blit(text, (last_cell_x + self.cell_size + 2 * self.margin, last_cell_y + self.cell_size // 2))

#     '''Shifted to Renderer'''
#     def render_game_over(self, message):
#         self.render_static_board()
#         font = pygame.font.Font(None, 50)
#         text = font.render(message, True, (98, 219, 89))  
#         text_rect = text.get_rect(center=(self.window_size // 2, self.window_size // 2))
#         self.screen.blit(text, text_rect)

#         button_font = pygame.font.Font(None, 36)
#         button_text = button_font.render("again?", True, (255, 255, 255))
        
#         self.restart_rect = pygame.Rect(self.window_size // 2 - 60, self.window_size // 2 + 30, 110, 60)

#         pygame.draw.rect(self.screen, (98, 219, 89), self.restart_rect)
#         self.screen.blit(button_text, button_text.get_rect(center=self.restart_rect.center))

#         return self.restart_rect
        
    




# board = Board()
# board.make_window()
# # print(board.grid)

# while True:

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
                
#         board.handle_events(event)

#     board.render_state()
#     pygame.display.update()
