"""
    Bomberman lives in a rectangular grid. Each cell in the grid either contains a bomb or
    nothing at all.
    Each bomb can be planted in any cell of the grid but once planted, it will detonate after
    exactly 3 seconds. Once a bomb detonates, it&#39;s destroyed — along with anything in its four
    neighboring cells. This means that if a bomb detonates in cell i, j, any valid cells ( i ± 1, j )
    and ( i, j ± 1 ) are cleared. If there is a bomb in a neighboring cell, the neighboring bomb is
    destroyed without detonating, so there&#39;s no chain reaction.
"""
import sys

def createGrid(r, c, grid_at_previous_step):
    grid_at_next_step = [['O'] * c for _ in range(r)]
    for i in range(r):
        for j in range(c):
            current_cell = grid_at_previous_step[i][j]
            if current_cell == 'O':
                grid_at_next_step[i][j] = '.'
                if i - 1 >= 0:
                    grid_at_next_step[i - 1][j] = '.'
                if i + 1 <= r - 1:
                    grid_at_next_step[i + 1][j] = '.'
                if j - 1 >= 0:
                    grid_at_next_step[i][j - 1] = '.'
                if j + 1 <= c - 1:
                    grid_at_next_step[i][j + 1] = '.'
    return grid_at_next_step


def bomberMan(n, r, c, initial_grid):

    grid_after_first_detonation = createGrid(r, c, initial_grid)

    if n % 2 == 0:
        return [['O'] * c for _ in range(r)]
    elif n < 4:
        return initial_grid if n == 1 else grid_after_first_detonation
    else:
        grid_after_second_detonation = createGrid(r, c, grid_after_first_detonation)
        grid_after_third_detonation = createGrid(r, c, grid_after_second_detonation)
        return grid_after_second_detonation if n % 4 == 1 else grid_after_third_detonation


if __name__ == "__main__":
    r, c, n = input().strip().split(' ')
    r, c, n = [int(r), int(c), int(n)]
    grid = []
    for _ in range(r):
       grid.append(list(str(input().strip())))
    result = bomberMan(n, r, c, grid)
    for row in result:
        print("".join(row))