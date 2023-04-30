import random
from random import choice
from copy import deepcopy

def play_game(board, player, show_output=True):
    """
    Play a game of tic-tac-toe on a given board between a Menace player and a random player.

    Parameters:
    board (list): A list of length 9 representing the tic-tac-toe board.
                  Each element in the list is either 'X', 'O', or '' (empty).
    player (dict): A dictionary representing the Menace player.
                    The keys of the dictionary are board configurations, and
                    the values are lists of length 9 representing the weights
                    associated with each move on that board.
    show_output (bool): A flag to indicate if the board should be printed during the game.

    Returns:
    str: The winner of the game ('X', 'O', or 'Draw').
    """

    menace_player = 'X'
    random_player = 'O'
    winner = None

    while winner is None:
        if menace_player == 'X':
            current_player_dict = player
        else:
            current_player_dict = {}

        board_config = tuple(board)

        if board_config in current_player_dict:
            weights = current_player_dict[board_config]
            empty_indices = [i for i in range(9) if board[i] == '']
            move_weights = [weights[i] for i in empty_indices]
            max_weight = max(move_weights)
            best_moves = [empty_indices[i] for i in range(len(empty_indices)) if move_weights[i] == max_weight]
            move = choice(best_moves)
        else:
            move = choice([i for i in range(9) if board[i] == ''])

        board[move] = menace_player
        current_player_dict[board_config][move] += 1

        if show_output:
            print(f"{menace_player}'s move:")
            print_board(board)

        if check_win(board):
            winner = menace_player
        elif '' not in board:
            winner = 'Draw'

        menace_player, random_player = random_player, menace_player

    if show_output:
        print(f"Game over. {winner} wins!")
        
    return winner

def print_board(board):
    print("-------------")
    for i in range(3):
        print("| {} | {} | {} |".format(board[i * 3], board[i * 3 + 1], board[i * 3 + 2]))
        print("-------------")

def choose_move_index(move_weights):
    """
    Select an index from the list of move weights using a weighted random choice.

    Parameters:
    move_weights (list): A list of weights representing the move probabilities.

    Returns:
    int: The index of the selected move.
    """

    if not move_weights:
        return None

    total_weight = sum(move_weights)
    threshold = random.uniform(0, total_weight)
    weight_sum = 0

    for i, weight in enumerate(move_weights):
        weight_sum += weight
        if weight_sum >= threshold:
            return i

def check_win(board):
    """
    Check if there is a winning configuration on the board.

    Parameters:
    board (list): A list of length 9 representing the current state of the board.

    Returns:
    str or None: The symbol of the winner ('X' or 'O') if there is a winner,
    None if the game is not over yet,
    'TIE' if the game is a tie.
    """
    # Check horizontal lines
    for i in range(0, 9, 3):
        if board[i] == board[i+1] == board[i+2] and board[i] != '':
            return board[i]

    # Check vertical lines
    for i in range(3):
        if board[i] == board[i+3] == board[i+6] and board[i] != '':
            return board[i]

    # Check diagonal lines
    if board[0] == board[4] == board[8] and board[0] != '':
        return board[0]

    if board[2] == board[4] == board[6] and board[2] != '':
        return board[2]

    # Check if there are empty cells left
    if '' in board:
        return None

    # If there are no empty cells left, the game is a tie
    return 'TIE'

def menace(num_episodes, show_output=True):
    """
    Train a Menace player through a number of games of tic-tac-toe.

    Parameters:
    num_episodes (int): The number of episodes (games) to play.
    show_output (bool): A flag to indicate if the board should be printed during the game.

    Returns:
    dict: A dictionary representing the trained Menace player.
          The keys of the dictionary are board configurations, and
          the values are lists of length 9 representing the weights
          associated with each move on that board.
    """

    player = {}

    for i in range(num_episodes):
        if show_output:
            print(f"Episode {i+1}/{num_episodes}")

        board = ['', '', '',
                 '', '', '',
                 '', '', '']

        moves = []

        while True:
            board_config = tuple(board)

            if board_config not in player:
                player[board_config] = [2] * 9

            weights = player[board_config]
            empty_indices = [i for i in range(9) if board[i] == '']
            move_weights = [weights[i] for i in empty_indices]

            if len(empty_indices) == 0:
                # Tie game
                if show_output:
                    print_board(board)
                    print("Tie game!")
                for move in moves:
                    player[move[0]][move[1]] += 1
                break

            move_index = choose_move_index(move_weights)
            if move_index is not None:
                move_position = empty_indices[move_index]
                moves.append((board_config, move_position))

            board[move_position] = 'X'

            if show_output:
                print_board(board)

            winner = check_win(board)
            if winner is not None:
                if show_output:
                    print("Winner:", winner)
                for move in moves:
                    player[move[0]][move[1]] += 3 if winner == 'X' else -1
                break

            move_weights = [weights[i] for i in range(9) if board[i] == '']
            if len(move_weights) == 0:
                # Tie game
                if show_output:
                    print_board(board)
                    print("Tie game!")
                for move in moves:
                    player[move[0]][move[1]] += 1
                break

            move_index = choose_move_index(move_weights)
            move_position = [i for i in range(9) if board[i] == ''][move_index]
            moves.append((board_config, move_position))

            board[move_position] = 'O'

            if show_output:
                print_board(board)

            winner = check_win(board)
            if winner is not None:
                if show_output:
                    print("Winner:", winner)
                for move in moves:
                    player[move[0]][move[1]] += 3 if winner == 'O' else -1
                break
    
    return player
    
trained_player = menace(num_episodes=100, show_output=False)
print(trained_player)


