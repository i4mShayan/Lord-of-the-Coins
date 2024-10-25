import pygame
import copy
from threading import Thread
import threading
from game.rendering import render, draw_agents_buttons, draw_next_button
from funcs import is_legal, move, check_winning
from agents.bfs import bfs
from agents.dfs import dfs
from agents.a_star import a_star
from tests.easy import easy
from tests.hard import hard
import pygame.gfxdraw
import time

# Global variables (Critical Section Handlers)
solution_ready = False
solution = None

# This function automatically executes moves stored in the list <moves>.
def automator(moves, state, screen, images, animPtr_ref, steps_list, level_index):
    for step in moves:
        pygame.time.wait(100)
        move(state, step)
        steps_list[0] += 1
        
        # Update the screen after each move
        screen.fill((53, 73, 94))
        animPtr_ref[0] += 1  # Update animation pointer
        render(state, screen, images, animPtr_ref[0])
        
        # Draw buttons and update the screen
        draw_agents_buttons(screen, images)

        # Render level number and steps on screen
        font = pygame.font.SysFont(None, 30)
        steps_text = font.render(f"Steps: {steps_list[0]}", True, (255, 255, 255))
        level_text = font.render(f"Level: {level_index + 1}", True, (255, 255, 255))
        
        # Display level number in the top-left
        screen.blit(level_text, (10, 10))
        # Display steps in the top-right corner
        screen.blit(steps_text, (screen.get_width() - steps_text.get_width() - 10, 10))
        
        pygame.display.update()
        pygame.time.wait(50) 

# Main game function that will initiate the game loop.
def gameScreen(curr_state, level_index, levels, images, sounds):
    buffer = 0
    animPtr_ref = [0]  # Using a list to pass by reference
    level_cleared = False
    steps_list = [0]  # Step counter as a mutable list
    solver_thread = None  # Thread for solving
    automator_moves = []  # List to hold automator moves
    automator_delay = 200  # Delay between automator moves in milliseconds
    last_move_time = 0  # Time when the last automator move was made
    global solution_ready, solution

    pygame.init()
    pygame.mixer.init()
   
    # Assign sounds
    push = sounds["push"]
    footstep = sounds["footstep"]
    metal = sounds["metal"]

    pygame.display.set_caption("Lord of the Coins")
    pygame.display.set_icon(images["icon"])
    screen2 = pygame.display.set_mode((416, 416))
    screen2.fill((53, 73, 94))
    end = False

    while not end:
        clock = pygame.time.Clock()
        clock.tick(24)
        
        # Start the automator if the solution is ready
        if solution_ready:
            solution_ready = False
            # print(f"Starting automator with solution: {solution}")  # Debug print
            automator_moves = solution.copy()
            solution = None
            last_move_time = pygame.time.get_ticks()

        # Process automator moves
        if automator_moves:
            current_time = pygame.time.get_ticks()
            if current_time - last_move_time >= automator_delay:
                step = automator_moves.pop(0)
                if is_legal(curr_state, step):
                    move(curr_state, step)
                    steps_list[0] += 1  # Increment steps after each move
                else:
                    print(f"Illegal move attempted: {step}")
                last_move_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True
            if event.type == pygame.KEYDOWN and not level_cleared and not automator_moves:
                step = None
                if event.key == pygame.K_UP:
                    step = (0, -1)
                elif event.key == pygame.K_DOWN:
                    step = (0, 1)
                elif event.key == pygame.K_LEFT:
                    step = (-1, 0)
                elif event.key == pygame.K_RIGHT:
                    step = (1, 0)
                
                if step and is_legal(curr_state, step):
                    target_y = curr_state.player_y + step[1]
                    target_x = curr_state.player_x + step[0]
                    target_cell = curr_state.grid[target_y][target_x]
                    
                    if target_cell == 0:
                        footstep.play()
                        pygame.mixer.music.stop()
                    elif target_cell == 2:
                        push.play()
                        pygame.mixer.music.stop()
                    elif target_cell == 3:
                        metal.play()
                        pygame.mixer.music.stop()
                    
                    move(curr_state, step)
                    steps_list[0] += 1  # Increment the step counter

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if level_cleared:
                    # Next Level Button
                    if 169 <= mouse[0] <= 247 and 360 <= mouse[1] <= 393:
                        level_cleared = False
                        level_index += 1
                        if level_index >= len(levels):
                            level_index = 0
                        curr_state = copy.deepcopy(levels[level_index])
                        steps_list[0] = 0  # Reset steps when moving to the next level
                else:
                    if not automator_moves:  # Prevent starting a new solution during automation
                        # BFS Button
                        if 45.5 <= mouse[0] <= 123.5 and 360 <= mouse[1] <= 393:
                            steps_list[0] = 0  # Reset steps when starting a new solution
                            curr_state = copy.deepcopy(levels[level_index])
                            # Start the BFS solver in a separate thread
                            solver_thread = threading.Thread(target=lambda: bfs_solution(curr_state))
                            solver_thread.start()
                        # A* Button
                        if 169 <= mouse[0] <= 247 and 360 <= mouse[1] <= 393:
                            steps_list[0] = 0  # Reset steps when starting a new solution
                            curr_state = copy.deepcopy(levels[level_index])
                            # Start the A* solver in a separate thread
                            solver_thread = threading.Thread(target=lambda: astar_solution(curr_state))
                            solver_thread.start()
                        # DFS Button
                        if 292.5 <= mouse[0] <= 370.5 and 360 <= mouse[1] <= 393:
                            steps_list[0] = 0  # Reset steps when starting a new solution
                            curr_state = copy.deepcopy(levels[level_index])
                            # Start the DFS solver in a separate thread
                            solver_thread = threading.Thread(target=lambda: dfs_solution(curr_state))
                            solver_thread.start()

        if check_winning(curr_state) and not level_cleared:
            level_cleared = True
            print(f"Level {level_index + 1} Done!\n" + "-" * 60)

        # Update animation pointer
        buffer += 1
        if buffer % 4 == 0:
            animPtr_ref[0] += 1

        # Render the current state
        screen2.fill((53, 73, 94))
        render(curr_state, screen2, images, animPtr_ref[0])
        
        # Render the level number and steps
        font = pygame.font.SysFont(None, 30)
        level_text = font.render(f"Level: {level_index + 1}", True, (255, 255, 255))
        steps_text = font.render(f"Steps: {steps_list[0]}", True, (255, 255, 255))
        
        # Display level number at (10, 10) (top-left)
        screen2.blit(level_text, (10, 10))

        # Display steps at the top-right corner
        screen2.blit(steps_text, (screen2.get_width() - steps_text.get_width() - 10, 10))
        
        if not level_cleared:
            draw_agents_buttons(screen2, images)  # Only show the buttons when the level isn't cleared
        else:
            draw_next_button(screen2, images)  # Show the 'Play Next' button
        
        pygame.display.update()

    pygame.quit()

def bfs_solution(curr_state):
    global solution_ready, solution
    print("Started BFS...")
    time_start = time.time()
    solution = bfs(curr_state).move_history
    print(f"Solved using BFS in {time.time() - time_start} seconds,")
    print(f"And in {len(solution)} steps.")
    solution_ready = True

def astar_solution(curr_state):
    global solution_ready, solution
    print("Started A*...")
    time_start = time.time()
    solution = a_star(curr_state).move_history
    print(f"Solved using A* in {time.time() - time_start} seconds,")
    print(f"And in {len(solution)} steps.")
    solution_ready = True

def dfs_solution(curr_state):
    global solution_ready, solution
    print("Started DFS...")
    time_start = time.time()
    solution = dfs(curr_state).move_history
    print(f"Solved using DFS in {time.time() - time_start} seconds.")
    print(f"And in {len(solution)} steps.")
    solution_ready = True

# Function to automate the moves based on the solution.
def automator(solution, curr_state, screen, images, animPtr_ref, steps_list, level_index):
    for step in solution:
        if is_legal(curr_state, step):
            move(curr_state, step)
            steps_list[0] += 1  # Increment steps after each move

            # Render the current state after each move
            screen.fill((53, 73, 94))
            render(curr_state, screen, images, animPtr_ref[0])

            # Render the level number and steps
            font = pygame.font.SysFont(None, 30)
            level_text = font.render(f"Level: {level_index + 1}", True, (255, 255, 255))
            steps_text = font.render(f"Steps: {steps_list[0]}", True, (255, 255, 255))
            screen.blit(level_text, (10, 10))
            screen.blit(steps_text, (screen.get_width() - steps_text.get_width() - 10, 10))

            # Update the display
            pygame.display.update()

            # Small delay to visualize the moves
            pygame.time.delay(200)  # Delay in milliseconds

        else:
            print(f"Illegal move attempted: {step}")


def draw_rounded_button(surface, rect, color, border_radius=10, shadow_offset=5):
    # Draw shadow
    shadow_rect = rect.move(shadow_offset, shadow_offset)
    pygame.draw.rect(surface, (50, 50, 50), shadow_rect, border_radius=border_radius)
    # Draw button
    pygame.draw.rect(surface, color, rect, border_radius=border_radius)
    # Draw 3D effect (lighter top part and darker bottom part)
    pygame.draw.rect(surface, (min(color[0] + 30, 255), min(color[1] + 30, 255), min(color[2] + 30, 255)), 
                     pygame.Rect(rect.x, rect.y, rect.width, rect.height // 2), border_radius=border_radius)
    pygame.draw.rect(surface, (max(color[0] - 30, 0), max(color[1] - 30, 0), max(color[2] - 30, 0)), 
                     pygame.Rect(rect.x, rect.y + rect.height // 2, rect.width, rect.height // 2), border_radius=border_radius)

#     Start screen function that displays the initial menu and handles user choices.
def startScreen(level_index, levels, images, sounds, fonts, background_path):
    end = False
    screen1 = pygame.display.set_mode((416, 416))
    pygame.display.set_caption("Lord of the Coins")
    pygame.display.set_icon(images["icon"])
    clock = pygame.time.Clock()

    # Load and scale the background image to fit the screen
    background_image = pygame.image.load(background_path).convert()
    background_image = pygame.transform.scale(background_image, (416, 416))

    pixel_font = fonts["text"]
    title_font = fonts["title"]
    small_font = pygame.font.Font(None, 18)  # Smaller font size for the copyright text
    
    # Colors
    text_color = (255, 229, 0)  # #FFE500
    button_color = (163, 128, 177)  # #A380B1
    button_hover_color = (183, 148, 197)
    title_color = button_color
    black_color = (0, 0, 0)  # Black for copyright text

    # Sizes and Offsets
    button_width, button_height = 140, 35
    title_y = 10
    button_y_offset = 80
    
    # Title box dimensions
    title_box_width, title_box_height = 320, 60
    
    while not end:
        clock.tick(30)
        
        # Display the background image
        screen1.blit(background_image, (0, 0))

        title_rect = pygame.Rect(416 // 2 - title_box_width // 2, title_y, title_box_width, title_box_height)
        draw_rounded_button(screen1, title_rect, title_color, border_radius=10)
        title = title_font.render('Lord of the Coins', True, text_color)
        title_text_rect = title.get_rect(center=title_rect.center)
        screen1.blit(title, title_text_rect)

        mouse = pygame.mouse.get_pos()

        # Button 1: Play (Easy)
        button1_rect = pygame.Rect(416 // 2 - button_width // 2, title_y + button_y_offset, button_width, button_height)
        button1_color = button_hover_color if button1_rect.collidepoint(mouse) else button_color
        draw_rounded_button(screen1, button1_rect, button1_color, border_radius=10)
        choice1 = pixel_font.render('Play (Easy)', True, text_color)
        choice1_rect = choice1.get_rect(center=button1_rect.center)
        screen1.blit(choice1, choice1_rect)

        # Button 2: Play (Hard)
        button2_rect = pygame.Rect(416 // 2 - button_width // 2, title_y + button_y_offset + 50, button_width, button_height)
        button2_color = button_hover_color if button2_rect.collidepoint(mouse) else button_color
        draw_rounded_button(screen1, button2_rect, button2_color, border_radius=10)
        choice2 = pixel_font.render('Play (Hard)', True, text_color)
        choice2_rect = choice2.get_rect(center=button2_rect.center)
        screen1.blit(choice2, choice2_rect)

        # Copyright text at the footer
        copyright_text = "SBU AI - Fall 2024"
        copyright_surface = small_font.render(copyright_text, True, black_color)
        copyright_rect = copyright_surface.get_rect(center=(416 // 2, 400))  # Center horizontally at the bottom
        screen1.blit(copyright_surface, copyright_rect)

        # Event handling for mouse click
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()

                # Play (Easy) 
                if button1_rect.collidepoint(mouse):
                    level_index = 0
                    levels = copy.deepcopy(easy)
                    curr_state = copy.deepcopy(levels[level_index])
                    gameScreen(curr_state, level_index, levels, images, sounds)
                    end = True

                # Play (Hard) 
                if button2_rect.collidepoint(mouse):
                    level_index = 0
                    levels = copy.deepcopy(hard)
                    curr_state = copy.deepcopy(levels[level_index])
                    gameScreen(curr_state, level_index, levels, images, sounds)
                    end = True

        pygame.display.update()
