import numpy as np

def get_next_state(current_state):
    next_state = np.copy(current_state)
    rows, cols = current_state.shape

    for row in range(rows):
        for col in range(cols):
            alive_neighbors = count_alive_neighbors(current_state, row, col)

            if current_state[row, col] == 1:
                if alive_neighbors < 2 or alive_neighbors > 3:
                    next_state[row, col] = 0
            else:
                if alive_neighbors == 3:
                    next_state[row, col] = 1

    return next_state

def count_alive_neighbors(state, row, col):
    alive_count = 0
    rows, cols = state.shape

    # Wrap around logic
    for i in range(row - 1, row + 2):
        for j in range(col - 1, col + 2):

            wrapped_row = i % rows
            wrapped_col = j % cols

            if (wrapped_row == row and wrapped_col == col):
                continue
            alive_count += state[wrapped_row, wrapped_col]

    return alive_count
