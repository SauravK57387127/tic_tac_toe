import pygame
from tic_tac_toe.game import Game


game = Game()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        game.handle_event(event)
    game.render()
    pygame.display.flip()

pygame.quit()

