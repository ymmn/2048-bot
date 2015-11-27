import time
import random
from p2048 import (
    RIGHT, DOWN, LEFT, UP,
    get_initial_board, execute_move, get_next_board
)


SLEEP_INTERVAL = 0


class TotallyRandomBot():
    def get_move(self, board):
        return random.choice([RIGHT, DOWN, LEFT, UP])


class SimplisticBot():
    def get_move(self, board):
        attempt_seq = [RIGHT, DOWN, LEFT]
        random.shuffle(attempt_seq)
        attempt_seq.append(UP)

        for move in attempt_seq:
            if get_next_board(board, move) != board:
                return move
        return move


class LookAheadBot():
    '''
    looks ahead n moves
    '''
    NUM_MOVES_TO_LOOK_AHEAD = 5

    def score_board_state(self, board):
        max_val = max([max([val for val in row if val] + [0]) for row in board])
        num_empty_squares = sum([row.count(None) for row in board])
        return max_val + num_empty_squares

    def get_best_move_and_score_n_moves_ahead(self, board, n):
        max_score = -1
        best_move = None

        for move in [RIGHT, DOWN, LEFT, UP]:
            new_board = get_next_board(board, move)
            is_dud = new_board == board
            if is_dud:
                continue

            if n > 1:
                _, score = self.get_best_move_and_score_n_moves_ahead(new_board, n - 1)
            else:
                score = self.score_board_state(new_board)

            if score > max_score and not is_dud:
                max_score = score
                best_move = move

        # look fewer steps if couldnt find a solution
        num_look_ahead = n - 2
        while max_score == -1 and num_look_ahead >= 0:
            best_move, max_score = self.get_best_move_and_score_n_moves_ahead(board, num_look_ahead)
            num_look_ahead -= 1

        return best_move, max_score

    def get_move(self, board):
        move, _ = self.get_best_move_and_score_n_moves_ahead(board, self.NUM_MOVES_TO_LOOK_AHEAD)
        return move


def execute_bot(bot):
    cur_board = get_initial_board()

    while True:
        next_move = bot.get_move(cur_board)
        cur_board = execute_move(cur_board, next_move)
        print ''
        print ''
        print ''
        if SLEEP_INTERVAL:
            time.sleep(SLEEP_INTERVAL)


def main():
    # execute_bot(SimplisticBot())
    # execute_bot(TotallyRandomBot())
    execute_bot(LookAheadBot())

main()
