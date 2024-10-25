class GameState:
    def __init__(self, grid, player_start_pos):
        self.grid = grid
        self.num_rows = len(grid)
        self.num_cols = len(grid[0])
        self.player_y = player_start_pos[0]
        self.player_x = player_start_pos[1]
        self.move_history = []