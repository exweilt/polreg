import pygame
import sys
from typing import Tuple

import utils
import polreg


# Define constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (40, 40, 40)

if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()

    # Create the display window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Polynomial Regression')
    font = pygame.font.Font(None, 40)  

    # Load points from dataset
    points: list[Tuple[float, float]] = utils.load_json_file()

    # Init the regression model and train it
    regression = polreg.PolynomialRegression(1, [1.0, 0.0], points)
    regression.train_complete_shuffle(1000000)

    # Main window loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #utils.save_points_to_json(points)
                pygame.quit()
                sys.exit()

            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     mouse_x, mouse_y = event.pos

            #     points.append(utils.screen_to_virtual_coords((mouse_x, mouse_y)))
                

        # Clear the screen
        screen.fill(BG_COLOR)
        
        utils.draw_axis(screen)

        # Scatter Plot all the data points
        for p in points:
            utils.draw_point_at_position(screen, p)

        function_label_surface = font.render(f"p(x)={regression.get_polynomial_string()}", True, (200, 200, 200))
        screen.blit(function_label_surface, (230, 20))

        function_label_surface = font.render(f"Loss(p)={regression.loss()}", True, (200, 200, 200))
        screen.blit(function_label_surface, (230, 50))

        utils.draw_function(screen, regression.predict)
        
        # Update the display
        pygame.display.flip()
