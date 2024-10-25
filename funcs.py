def check_winning(state):
    won = True
    for i in range(0, state.num_rows):
        for j in range(0, state.num_cols):
            if state.grid[i][j] == 2:
                won = False
    return won

def move(state, step):
    if state.grid[state.player_y+step[1]][state.player_x+step[0]] == 0 or state.grid[state.player_y+step[1]][state.player_x+step[0]] == 2:
        state.player_y += step[1]
        state.player_x += step[0]
        state.move_history.append(step)
    else:
        state.grid[state.player_y+step[1]][state.player_x+step[0]] -= 3
        state.grid[state.player_y+2*step[1]][state.player_x+2*step[0]] += 3
        state.player_y += step[1]
        state.player_x += step[0]
        state.move_history.append(step)

def is_legal(state, step):
    if state.grid[state.player_y + step[1]][state.player_x + step[0]] == 1:
        return False
    elif state.grid[state.player_y + step[1]][state.player_x + step[0]] == 2 or state.grid[state.player_y + step[1]][state.player_x + step[0]] == 0:
        return True
    elif state.grid[state.player_y + 2 * step[1]][state.player_x + 2 * step[0]] != 1 and state.grid[state.player_y + 2 * step[1]][state.player_x + 2 * step[0]] < 3:
        return True
    return False

def is_blocked(state, step):
    if state.grid[state.player_y + step[1]][state.player_x + step[0]] == 3 and state.grid[state.player_y + 2 * step[1]][state.player_x + 2 * step[0]] != 2:
        if (state.grid[state.player_y + 2 * step[1] + 1][state.player_x + 2 * step[0]] == 1 and state.grid[state.player_y + 2 * step[1]][state.player_x + 2 * step[0] + 1] == 1):
            return True
        elif (state.grid[state.player_y + 2 * step[1] + 1][state.player_x + 2 * step[0]] == 1 and state.grid[state.player_y + 2 * step[1]][state.player_x + 2 * step[0] - 1] == 1):
            return True    
        elif (state.grid[state.player_y + 2 * step[1] - 1][state.player_x + 2 * step[0]] == 1 and state.grid[state.player_y + 2 * step[1]][state.player_x + 2 * step[0] + 1] == 1):
            return True   
        elif (state.grid[state.player_y + 2 * step[1] - 1][state.player_x + 2 * step[0]] == 1 and state.grid[state.player_y + 2 * step[1]][state.player_x + 2 * step[0] - 1] == 1):
            return True  
    return False