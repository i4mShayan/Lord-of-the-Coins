import pygame

# This function returns type of wall based on its position
def wall_interface_type(grid, pos):
    res = []
    if pos[0] > 0 and grid[pos[0]-1][pos[1]] not in (1, 6):
        res.append((-1, 0))
    if pos[0] < len(grid)-1 and grid[pos[0]+1][pos[1]] not in (1, 6):
        res.append((1, 0))
    if pos[1] > 0 and grid[pos[0]][pos[1]-1] not in (1, 6):
        res.append((0, -1))
    if pos[1] < len(grid[0])-1 and grid[pos[0]][pos[1]+1] not in (1, 6):
        res.append((0, 1))
    return res

# This function helps in the rendering of each item onto the screen
def render(curr_state, screen, images, animPtr):
    x = (416 - 32 * curr_state.num_rows) // 2
    for i in range(0, curr_state.num_rows):
        y = (416 - 32 * curr_state.num_cols) // 2
        for j in range(0, curr_state.num_cols):
            cell = curr_state.grid[i][j]
            if cell == 1:
                wall_type = wall_interface_type(curr_state.grid, (i, j))
                if len(wall_type) == 1:
                    if (i + j) % 2 == 0:
                        screen.blit(images["ground_d"][(i * j) % 2], (y, x))
                    else:
                        screen.blit(images["ground_l"][(i * j) % 2], (y, x))
                    if (0, 1) in wall_type:
                        screen.blit(images["wall_l"], (y, x))
                    elif (0, -1) in wall_type:
                        screen.blit(images["wall_r"], (y, x))
                    elif (1, 0) in wall_type:
                        screen.blit(images["wall_t"], (y, x))
                    elif (-1, 0) in wall_type:
                        screen.blit(images["wall_b"], (y, x))
                elif len(wall_type) == 2:
                    if (i + j) % 2 == 0:
                        screen.blit(images["ground_d"][(i * j) % 2], (y, x))
                    else:
                        screen.blit(images["ground_l"][(i * j) % 2], (y, x))
                    if (0, 1) in wall_type:
                        if (1, 0) in wall_type:
                            screen.blit(images["wall_lt"], (y, x))
                        elif (-1, 0) in wall_type:
                            screen.blit(images["wall_lb"], (y, x))
                        else:
                            screen.blit(images["wall_tb"], (y, x))
                    elif (0, -1) in wall_type:
                        if (1, 0) in wall_type:
                            screen.blit(images["wall_rt"], (y, x))
                        elif (-1, 0) in wall_type:
                            screen.blit(images["wall_rb"], (y, x))
                    else:
                        screen.blit(images["wall_lr"], (y, x))
                elif len(wall_type) == 3:
                    if (i + j) % 2 == 0:
                        screen.blit(images["ground_d"][(i * j) % 2], (y, x))
                    else:
                        screen.blit(images["ground_l"][(i * j) % 2], (y, x))
                    if (0, 1) not in wall_type:
                        screen.blit(images["wall_3r"], (y, x))
                    elif (0, -1) not in wall_type:
                        screen.blit(images["wall_3l"], (y, x))
                    elif (1, 0) not in wall_type:
                        screen.blit(images["wall_3b"], (y, x))
                    elif (-1, 0) not in wall_type:
                        screen.blit(images["wall_3t"], (y, x))
                elif len(wall_type) == 4:
                    if (i + j) % 2 == 0:
                        screen.blit(images["ground_d"][(i * j) % 2], (y, x))
                    else:
                        screen.blit(images["ground_l"][(i * j) % 2], (y, x))
                    screen.blit(images["wall_4"], (y, x))

            elif cell == 5:
                if (i + j) % 2 == 0:
                    if curr_state.grid[i-1][j] == 1:
                        screen.blit(images["ground_ds"][(i * j) % 2], (y, x))
                    else:
                        screen.blit(images["ground_d"][(i * j) % 2], (y, x))
                else:
                    if curr_state.grid[i-1][j] == 1:
                        screen.blit(images["ground_ls"][(i * j) % 2], (y, x))
                    else:
                        screen.blit(images["ground_l"][(i * j) % 2], (y, x))
                screen.blit(images["treasure"], (y, x))
            elif cell == 2:
                if (i + j) % 2 == 0:
                    if curr_state.grid[i-1][j] == 1:
                        screen.blit(images["ground_ds"][(i * j) % 2], (y, x))
                    else:
                        screen.blit(images["ground_d"][(i * j) % 2], (y, x))
                else:
                    if curr_state.grid[i-1][j] == 1:
                        screen.blit(images["ground_ls"][(i * j) % 2], (y, x))
                    else:
                        screen.blit(images["ground_l"][(i * j) % 2], (y, x))
                if (curr_state.player_y == i-1 and curr_state.player_x == j):
                    screen.blit(images["char_s"], (y, x))
                screen.blit(images["coin"][animPtr % 8], (y, x))
            elif cell == 3:
                if (i + j) % 2 == 0:
                    if curr_state.grid[i-1][j] == 1:
                        screen.blit(images["ground_ds"][(i * j) % 2], (y, x))
                    else:
                        screen.blit(images["ground_d"][(i * j) % 2], (y, x))
                else:
                    if curr_state.grid[i-1][j] == 1:
                        screen.blit(images["ground_ls"][(i * j) % 2], (y, x))
                    else:
                        screen.blit(images["ground_l"][(i * j) % 2], (y, x))
                screen.blit(images["crate"], (y, x))
            elif cell == 0:
                if (i + j) % 2 == 0:
                    if curr_state.grid[i-1][j] == 1:
                        screen.blit(images["ground_ds"][(i * j) % 2], (y, x))
                    else:
                        screen.blit(images["ground_d"][(i * j) % 2], (y, x))
                else:
                    if curr_state.grid[i-1][j] == 1:
                        screen.blit(images["ground_ls"][(i * j) % 2], (y, x))
                    else:
                        screen.blit(images["ground_l"][(i * j) % 2], (y, x))
                if (curr_state.player_y == i-1 and curr_state.player_x == j):
                    screen.blit(images["char_s"], (y, x))

            # Draw the player character
            if (curr_state.player_x == j and curr_state.player_y == i):
                screen.blit(images["character"][animPtr % 2], (y, x))

            y += 32
        x += 32

def draw_agents_buttons(screen, images):
    screen.blit(images["bfs_button"], (45.5, 360))
    screen.blit(images["a_star_button"], (169, 360))
    screen.blit(images["dfs_button"], (292.5, 360))

def draw_next_button(screen, images):
    screen.blit(images["next_button"], (169, 360))