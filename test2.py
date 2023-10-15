from collections import Counter

BOARD_EMPTY = 0
BOARD_PLAYER_X = 1
BOARD_PLAYER_O = -1

# Define the board size (5x5)
BOARD_SIZE = 5

def player(s):
    counter = Counter(s)
    x_places = counter[1]
    o_places = counter[-1]

    if x_places + o_places == BOARD_SIZE * BOARD_SIZE:
        return None
    elif x_places > o_places:
        return BOARD_PLAYER_O
    else:
        return BOARD_PLAYER_X

def actions(s):
    play = player(s)
    actions_list = [(play, i) for i in range(len(s)) if s[i] == BOARD_EMPTY]
    return actions_list

def result(s, a):
    (play, index) = a
    s_copy = s.copy()
    s_copy[index] = play
    return s_copy

def terminal(s):
    # Check rows and columns for a win
    for i in range(BOARD_SIZE):
        if all(s[i * BOARD_SIZE + j] == s[i * BOARD_SIZE] and s[i * BOARD_SIZE] != BOARD_EMPTY for j in range(BOARD_SIZE)):
            return s[i * BOARD_SIZE]

        if all(s[i + j * BOARD_SIZE] == s[i] and s[i] != BOARD_EMPTY for j in range(BOARD_SIZE)):
            return s[i]

    # Check diagonals for a win
    if all(s[i * BOARD_SIZE + i] == s[0] and s[0] != BOARD_EMPTY for i in range(BOARD_SIZE)):
        return s[0]

    if all(s[i * BOARD_SIZE + (BOARD_SIZE - 1 - i)] == s[BOARD_SIZE - 1] and s[BOARD_SIZE - 1] != BOARD_EMPTY for i in range(BOARD_SIZE)):
        return s[BOARD_SIZE - 1]

    if player(s) is None:
        return 0

    return None

def utility(s, cost):
    term = terminal(s)
    if term is not None:
        return (term, cost)

    action_list = actions(s)
    utils = []
    for action in action_list:
        new_s = result(s, action)
        utils.append(utility(new_s, cost + 1))

    score = utils[0][0]
    idx_cost = utils[0][1]
    play = player(s)
    if play == BOARD_PLAYER_X:
        for i in range(len(utils)):
            if utils[i][0] > score:
                score = utils[i][0]
                idx_cost = utils[i][1]
    else:
        for i in range(len(utils)):
            if utils[i][0] < score:
                score = utils[i][0]
                idx_cost = utils[i][1]
    return (score, idx_cost)

def minimax(s):
    action_list = actions(s)
    utils = []
    for action in action_list:
        new_s = result(s, action)
        utils.append((action, utility(new_s, 1)))

    if len(utils) == 0:
        return ((0, 0), (0, 0))

    sorted_list = sorted(utils, key=lambda l: l[0][1])
    action = min(sorted_list, key=lambda l: l[1])
    return action

def print_board(s):
    def convert(num):
        if num == BOARD_PLAYER_X:
            return 'X'
        if num == BOARD_PLAYER_O:
            return 'O'
        return '_'

    i = 0
    for _ in range(BOARD_SIZE):
        for _ in range(BOARD_SIZE):
            print(convert(s[i]), end=' ')
            i += 1
        print()

if __name__ == '__main__':
    s = [BOARD_EMPTY for _ in range(BOARD_SIZE * BOARD_SIZE)]
    print(f'|------- WELCOME TO {BOARD_SIZE}x{BOARD_SIZE} TIC TAC TOE -----------|')
    print('You are X while the Computer is O')

    while terminal(s) is None:
        play = player(s)
        if play == BOARD_PLAYER_X:
            print('\n\nIt is your turn', end='\n\n')
            x = int(input(f'Enter the row coordinate [0-{BOARD_SIZE - 1}]: '))
            y = int(input(f'Enter the column coordinate [0-{BOARD_SIZE - 1}]: '))
            index = BOARD_SIZE * x + y

            if not s[index] == BOARD_EMPTY:
                print('That coordinate is already taken. Please try again.')
                continue

            s = result(s, (1, index))
            print_board(s)
        else:
            print('\n\nThe computer is playing its turn')
            action = minimax(s)
            s = result(s, action[0])
            print_board(s)

    winner = utility(s, 1)[0]
    if winner == BOARD_PLAYER_X:
        print("You have won!")
    elif winner == BOARD_PLAYER_O:
        print("You have lost!")
    else:
        print("It's a tie.")
