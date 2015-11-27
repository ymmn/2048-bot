import random
import copy


# moves
RIGHT = 100
LEFT = 101
DOWN = 102
UP = 103
INITIAL = 104

NUM_ROWS = 4
NUM_COLS = 4

DETERMINISTIC = False

INPUT_MAP = {
    'r': RIGHT,
    'l': LEFT,
    'd': DOWN,
    'u': UP,
}


def get_board_sum(board):
    return sum([sum([val for val in row if val]) for row in board])


def attempt_combine(val1, val2):
    if val1 is None or val2 is None:
        raise ValueError('not supposed to get None in attempt_combine')

    if val1 == val2:
        return val1 * 2, True
    else:
        return None, False


def combine_value_array(old_vals, left_join=True):
    '''
    take something like [2, 2, 2] and return [4, 2] or [2, 4]
    '''
    assert None not in old_vals and len(old_vals) > 1

    new_vals = []
    val_idx = 0
    while val_idx < len(old_vals):
        if val_idx == len(old_vals) - 1:
            new_vals.append(old_vals[val_idx])
            break

        new_val, combined = attempt_combine(
            old_vals[val_idx], old_vals[val_idx + 1]
        )
        if combined:
            # skip next iteration
            new_vals.append(new_val)
            val_idx += 2
            continue

        new_vals.append(old_vals[val_idx])
        val_idx += 1

    return new_vals


def perform_move_on_board(cur_board, move):
    is_horizontal_move = move in (RIGHT, LEFT)
    is_vertical_move = move in (UP, DOWN)
    is_dud_move = False
    if is_horizontal_move:
        is_dud_move = True
        for row_idx in range(NUM_ROWS):
            non_empty_values = [val for val in cur_board[row_idx] if val]
            can_combine_stuff = len(non_empty_values) > 1
            if can_combine_stuff:
                new_vals = combine_value_array(non_empty_values)
            else:
                new_vals = non_empty_values

            is_dud_move = is_dud_move and (len(non_empty_values) in (0, NUM_COLS) and non_empty_values == new_vals)

            num_cells_to_pad = NUM_COLS - len(new_vals)
            for _ in range(num_cells_to_pad):
                if move == LEFT:
                    new_vals.append(None)
                else:
                    new_vals.insert(0, None)

            cur_board[row_idx] = new_vals
    elif is_vertical_move:
        # TODO(abdul) this aint dry
        is_dud_move = True
        for col_idx in range(NUM_COLS):
            non_empty_values = [cur_board[row_idx][col_idx] for row_idx in range(NUM_ROWS)
                                if cur_board[row_idx][col_idx]]

            can_combine_stuff = len(non_empty_values) > 1
            if can_combine_stuff:
                new_vals = combine_value_array(non_empty_values)
            else:
                new_vals = non_empty_values

            is_dud_move = is_dud_move and (len(non_empty_values) in (0, NUM_ROWS) and non_empty_values == new_vals)

            num_cells_to_pad = NUM_ROWS - len(new_vals)
            for _ in range(num_cells_to_pad):
                if move == UP:
                    new_vals.append(None)
                else:
                    new_vals.insert(0, None)

            for row_idx in range(NUM_ROWS):
                cur_board[row_idx][col_idx] = new_vals[row_idx]

    return cur_board


def get_empty_row_cols(board):
    empty_row_cols = []
    for row_idx in range(NUM_ROWS):
        for col_idx in range(NUM_COLS):
            if board[row_idx][col_idx] is None:
                empty_row_cols.append((row_idx, col_idx))
    return empty_row_cols


def get_next_board(old_board, move, populate_empty_square=True):
    # first combine adjacent squares either vertically or horizontally
    # then move everything
    old_board_sum = get_board_sum(old_board)

    new_board = perform_move_on_board(copy.deepcopy(old_board), move)

    if populate_empty_square:
        empty_row_cols = get_empty_row_cols(new_board)

        # move is None on initialization
        is_dud_move = (new_board == old_board and move != INITIAL)
        if is_dud_move:
            return new_board

        if empty_row_cols:
            if DETERMINISTIC:
                row_col_to_populate = empty_row_cols[0]
            else:
                row_col_to_populate = random.choice(empty_row_cols)

            new_board[row_col_to_populate[0]][row_col_to_populate[1]] = 2

        assert get_board_sum(new_board) == old_board_sum + 2
    else:
        assert get_board_sum(new_board) == old_board_sum

    return new_board


def check_game_over(board):
    for move in (UP, DOWN, LEFT, RIGHT):
        new_board = perform_move_on_board(copy.deepcopy(board), move)
        if new_board != board:
            return False

    return True


def print_board(board):
    divider = '=' * 27

    for row in board:
        print divider
        print '|'.join(' %4s ' % col for col in row)

    print divider


def execute_move(cur_board, move):
    new_board = get_next_board(cur_board, move)
    print_board(new_board)

    is_dud_move = new_board == cur_board
    if is_dud_move:
        is_game_over = not get_empty_row_cols(new_board) and check_game_over(new_board)
        if is_game_over:
            print 'game over'
            print 'total score: ', get_board_sum(new_board)
            exit(0)

        print 'dud. try again'

    max_val = max([max([val for val in row if val] + [0]) for row in new_board])
    if max_val >= 2048:
        print 'you win!'
        exit(0)

    return new_board


def get_initial_board():
    initial_board = []
    for _ in range(NUM_ROWS):
        initial_board.append([None] * NUM_COLS)

    return get_next_board(initial_board, INITIAL)


def main():
    cur_board = get_initial_board()
    print_board(cur_board)

    while True:
        next_move = None
        while next_move is None:
            next_move = INPUT_MAP.get(raw_input())
            if next_move is None:
                print 'use "r", "u", "l", and "d"'
        cur_board = execute_move(cur_board, next_move)

# main()
