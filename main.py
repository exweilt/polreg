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
HELP_LABEL_COLOR = (120, 120, 120)

if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()

    # Create the display window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Polynomial Regression')
    font = pygame.font.Font(None, 40)  

    # Load points from dataset
    points: list[Tuple[float, float]] = utils.load_json_file("data.json")
    points = utils.normalize_dataset(points)

    a, b = polreg.gradient_descent(points, 0.01, 10000)
    # Init the regression model and train it
    regression = polreg.PolynomialRegression(1, [a, b], points)
    # regression.train_complete_shuffle(10000)
    # regression.train_gradient_descent(10)

    # Prerender Help labels
    help_font = pygame.font.Font(None, 20)  
    help_label1 = help_font.render(f"<p> put a point", True, HELP_LABEL_COLOR)
    help_label2 = help_font.render(f"<s> save points to file", True, HELP_LABEL_COLOR)
    help_label3 = help_font.render(f"<LMB> drag", True, HELP_LABEL_COLOR)

    # Main window loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Keyboard Handler
            if event.type == pygame.KEYDOWN:
                # Add point under cursor <p>
                if event.key == pygame.K_p:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    points.append(utils.screen_to_virtual_coords((mouse_x, mouse_y)))

                # Save points to file <s>
                elif event.key == pygame.K_s:
                    utils.save_points_to_json(points, "data.json")
                
                # Save points to file <Esc>
                elif event.key == pygame.K_ESCAPE:
                    running = False
            
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    utils.virtual_origin_pos_shift = (
                        utils.virtual_origin_pos_shift[0] + event.rel[0],
                        utils.virtual_origin_pos_shift[1] - event.rel[1],
                    )
                
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

        # Draw help labels
        cursor_pos = utils.screen_to_virtual_coords(pygame.mouse.get_pos())
        help_label4 = help_font.render(f"cursor pos: x={    \
                cursor_pos[0]:.1f
            } y={
                cursor_pos[1]:.1f
            }", True, HELP_LABEL_COLOR)
        
        screen.blit(help_label1, (10, 10))
        screen.blit(help_label2, (10, 30))
        screen.blit(help_label3, (10, 50))
        screen.blit(help_label4, (10, 70))
        
        # Update the display
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()
