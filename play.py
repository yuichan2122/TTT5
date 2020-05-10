from TTT5 import TTT5
import numpy as np
from tensorflow.keras.models import load_model


def get_state(board, player):
    state = []
    for loc in board:
        state.append(loc)
        state.append(player)
    state = np.array(state).reshape((5, 5, 2))
    return np.array([state])


def main():
    end = False
    while not end:
        player_turn = board.player
        if player_turn == first:
            if mode == 1:
                board.print_board()
                ret = board.play(int(input('Human turn:')))
                if 'invalid' in ret:
                    print('Invalid move. Try again')
                if 'win' in ret:
                    print('Human win')
                if 'draw' in ret:
                    print('draw')
            else:
                state = get_state(board.board[:], int(player_turn))
                output = model.predict(np.array(state))
                if print_output:
                    print(np.round(output[0][0:5], 2))
                    print(np.round(output[0][5:10], 2))
                    print(np.round(output[0][10:15], 2))
                    print(np.round(output[0][15:20], 2))
                    print(np.round(output[0][20:25], 2))
                if board.played == 0:
                    action = 12
                else:
                    action = np.argmax(output)
                ret = board.play(action)
                if 'invalid' in ret:
                    board.print_board()
                    print('Invalid move. AI lose')
                    exit()
                if 'win' in ret:
                    print('Ai win')
                if 'draw' in ret:
                    print('draw')
        else:
            board.print_board()
            ret = board.play(int(input('Human turn:'))-1)
            if 'invalid' in ret:
                print('Invalid move. Try again')
            if 'win' in ret:
                print('Human win')
            if 'draw' in ret:
                print('draw')
        if 'win' in ret or 'draw' in ret:
            board.print_board()
            end = True


first = 1  # 1:ai first, 2:human first
mode = 2  # 1:human, 2:AI
name = 'CNN_240004_9'
if mode == 2:
    model = load_model(f'keras_model/{name}')
board = TTT5()
print_output = True
if __name__ == '__main__':
    main()
'''
1  2  3  4  5   
6  7  8  9  10 
11 12 13 14 15 
16 17 18 19 20 
21 22 23 24 25
'''
