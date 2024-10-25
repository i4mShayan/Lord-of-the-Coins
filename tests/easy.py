from game_state import GameState

g1 =[[6, 6, 1, 1, 1, 6, 6, 6],
      [6, 6, 1, 2, 1, 6, 6, 6],
      [6, 6, 1, 0, 1, 1, 1, 1],
      [1, 1, 1, 3, 0, 3, 2, 1],
      [1, 2, 0, 3, 0, 1, 1, 1],
      [1, 1, 1, 1, 3, 1, 6, 6],
      [6, 6, 6, 1, 2, 1, 6, 6],
      [6, 6, 6, 1, 1, 1, 6, 6]]

g2 = [[1, 1, 1, 1, 6, 6],
      [1, 0, 0, 1, 1, 1],
      [1, 0, 1, 0, 0, 1],
      [1, 0, 3, 5, 0, 1],
      [1, 0, 2, 5, 0, 1],
      [1, 0, 0, 0, 0, 1],
      [1, 1, 1, 1, 1, 1]]

g3 = [[1, 1, 1, 6, 6, 6],
      [1, 0, 2, 1, 6, 6],
      [1, 0, 0, 1, 1, 1],
      [1, 5, 0, 0, 0, 1],
      [1, 0, 0, 3, 0, 1],
      [1, 0, 0, 1, 1, 1],
      [1, 1, 1, 1, 6, 6]]

l1 = GameState(g1, (4, 4))
l2 = GameState(g2, (2, 3))
l3 = GameState(g3, (3, 2))

easy = [l1, l2, l3]