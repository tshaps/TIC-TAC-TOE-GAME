""" TIC-TAC-TOE-GAME
This is a text-based version of Tic-Tac-Toe Game
"""
# Importing randint from the random module
from random import randint
import time

# Create a list for the board blocks with spaces inside
board_list = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]

# Create an empty board
board = f"""
\033[4m{board_list[0][0]}|{board_list[0][1]}|{board_list[0][2]}\033[0m
\033[4m{board_list[1][0]}|{board_list[1][1]}|{board_list[1][2]}\033[0m
{board_list[2][0]}|{board_list[2][1]}|{board_list[2][2]}
"""

# Created a nested list of possible winning combos
win_combos = [
    [board_list[0][0], board_list[0][1], board_list[0][2]],
    [board_list[1][0], board_list[1][1], board_list[1][2]],
    [board_list[2][0], board_list[2][1], board_list[2][2]],
    [board_list[0][0], board_list[1][0], board_list[2][0]],
    [board_list[0][1], board_list[1][1], board_list[2][1]],
    [board_list[0][2], board_list[1][2], board_list[2][2]],
    [board_list[0][0], board_list[1][1], board_list[2][2]],
    [board_list[0][2], board_list[1][1], board_list[2][0]]
]

# Create a list of possible moves
possible_moves = [
    (0, 0),
    (0, 1),
    (0, 2),
    (1, 0),
    (1, 1),
    (1, 2),
    (2, 0),
    (2, 1),
    (2, 2)
]

# Scores Variables
player_score = 0
computer_score = 0

is_game_on = True


# Function to prompt user to play again
def play_again():
    response = input('Do you want to play again? (Y/N): ').upper()
    return response == 'Y'


# This function updates the board with the user and computer selected move using the maker
def move(moves, selection, maker):
    while True:
        if selection in moves:
            board_list[selection[0]][selection[1]] = maker
            moves.remove(selection)

            global board
            board = f"""
            \033[4m{board_list[0][0]}|{board_list[0][1]}|{board_list[0][2]}\033[0m
            \033[4m{board_list[1][0]}|{board_list[1][1]}|{board_list[1][2]}\033[0m
            {board_list[2][0]}|{board_list[2][1]}|{board_list[2][2]}
            """
            global win_combos
            win_combos = update_win_combos()
            return board
        else:
            print("Sorry, the block is not empty. Try again.")
            selection = player_func()


def player_func():
    """ This function prompts the user for the selection and returns the user's selected move """
    player_select = input('Its your move: (e.g. For top left corner 1,1): ')
    player_row = int(player_select.split(",")[0]) - 1
    player_col = int(player_select.split(',')[1]) - 1
    player_selection = (player_row, player_col)
    return player_selection


def computer_easy_level():
    """ This function creates a random selection for the computer and returns the selection """
    print("Computer's move: ")
    # Check if there are still moves available in the possible moves list
    if len(possible_moves) > 0:
        # Generates a random number within the length of the possible moves list
        random_move = randint(0, len(possible_moves) - 1)
        # Using the random_move it selects the move from possible_moves list
        comp_selection = possible_moves[random_move]
        return comp_selection


def computer_hard_level(player_maker, comp_maker):
    """ This function is for the computer hard level move, it checks for the possible win move first, then block move
    to prevent the player from winning, then check for the strategic move, if all fails it plays a random move"""
    # Define mappings for each win_combo to the actual board coordinates in possible_moves
    win_combos_positions = [
        [(0, 0), (0, 1), (0, 2)],  # First row
        [(1, 0), (1, 1), (1, 2)],  # Second row
        [(2, 0), (2, 1), (2, 2)],  # Third row
        [(0, 0), (1, 0), (2, 0)],  # First column
        [(0, 1), (1, 1), (2, 1)],  # Second column
        [(0, 2), (1, 2), (2, 2)],  # Third column
        [(0, 0), (1, 1), (2, 2)],  # Diagonal from top-left to bottom-right
        [(0, 2), (1, 1), (2, 0)]  # Diagonal from top-right to bottom-left
    ]

    # 1. Check for winning moves first
    for idx, win_combo in enumerate(win_combos):
        # Check for 2 "O" and 1 empty slot to win
        if win_combo.count(comp_maker) == 2 and win_combo.count(" ") == 1:
            empty_index = win_combo.index(" ")
            empty_move = win_combos_positions[idx][empty_index]
            if empty_move in possible_moves:
                print("Winning move:", empty_move)
                return empty_move  # Win the game

    # 2. Check for blocking moves if no winning move is found
    for idx, win_combo in enumerate(win_combos):
        # Check for 2 "X" and 1 empty slot to block the opponent
        if win_combo.count(player_maker) == 2 and win_combo.count(" ") == 1:
            empty_index = win_combo.index(" ")
            empty_move = win_combos_positions[idx][empty_index]
            if empty_move in possible_moves:
                print("Blocking move:", empty_move)
                return empty_move  # Block the opponent

    # 3. Check for strategic moves if no winning or blocking move is found
    for idx, win_combo in enumerate(win_combos):
        # Check for 2 empty spaces and 1 "O" to create a strategic move
        if win_combo.count(" ") == 2 and win_combo.count(comp_maker) == 1:
            o_index = win_combo.index(comp_maker)
            if o_index == 2 and win_combo[0] == " " and win_combo[1] == " ":
                empty_move = win_combos_positions[idx][0]
            elif o_index == 0 and win_combo[1] == " " and win_combo[2] == " ":
                empty_move = win_combos_positions[idx][2]
            else:
                empty_move = win_combos_positions[idx][0]

            if empty_move in possible_moves:
                print("Strategic move:", empty_move)
                return empty_move  # Play strategically

    # 4. If no winning, blocking, or strategic move is found, pick a random available move
    if possible_moves:
        random_move = possible_moves[randint(0, len(possible_moves) - 1)]
        print("Random move:", random_move)
        return random_move
    return None


def update_win_combos():
    return [
        [board_list[0][0], board_list[0][1], board_list[0][2]],
        [board_list[1][0], board_list[1][1], board_list[1][2]],
        [board_list[2][0], board_list[2][1], board_list[2][2]],
        [board_list[0][0], board_list[1][0], board_list[2][0]],
        [board_list[0][1], board_list[1][1], board_list[2][1]],
        [board_list[0][2], board_list[1][2], board_list[2][2]],
        [board_list[0][0], board_list[1][1], board_list[2][2]],
        [board_list[0][2], board_list[1][1], board_list[2][0]]
    ]


# Check if there are moves available
def moves_available():
    if len(possible_moves) == 0:
        print("Game Over! No moves left.")
        return False
    return True


# Check each winning combination for a winner
def check_winner(player_marker, computer_marker):
    """Check each winning combination for a winner."""
    for combo in win_combos:
        if all(item == player_marker for item in combo):
            return "Player"
        elif all(item == computer_marker for item in combo):
            return "Computer"
    return None


# Executes a player's turn and check for game status
def player_turn(player_func, maker):
    """Executes the player's turn and checks for game status"""
    if not moves_available():
        return False

    player_move = move(possible_moves, player_func(), maker)
    print(player_move)

    winner = check_winner(maker, 'O' if maker == 'X' else 'X')
    if winner:
        print(f"Player {winner} wins!")
        return winner
    if not moves_available():
        print("No more moves available.")
        return False
    return True


def computer_turn(level, player_maker, computer_marker):
    """Executes the computer's turn based on the selected difficulty level"""
    if not moves_available():
        return False

    # Select move based on level
    computer_move = computer_easy_level() if level == 'E' else computer_hard_level(player_maker, computer_marker)
    move(possible_moves, computer_move, computer_marker)
    print(board)

    winner = check_winner(player_maker, computer_marker)
    if winner:
        print(f"Player {winner} wins!")
        return winner
    if not moves_available():
        print("No more moves available.")
        return False
    return True


def game_play(level, first_player, player_marker, computer_marker):
    """Main game loop"""
    global is_game_on, win_combos, board_list
    reset_board()

    while is_game_on:
        win_combos = update_win_combos()

        if not moves_available():
            break

        # Player's move
        if first_player == "P":
            if player_turn(player_func, player_marker):
                winner = check_winner(player_marker, computer_marker)
                if winner:
                    print(f"\n{winner} wins the game!")
                    return winner
            if computer_turn(level, player_marker, computer_marker):
                winner = check_winner(player_marker, computer_marker)
                if winner:
                    print(f"\n{winner} wins the game!")
                    return winner

        elif first_player == 'C':
            if computer_turn(level, player_marker, computer_marker):
                winner = check_winner(player_marker, computer_marker)
                if winner:
                    print(f"\n{winner} wins the game!")
                    return winner
            if player_turn(player_func, player_marker):
                winner = check_winner(player_marker, computer_marker)
                if winner:
                    print(f"\n{winner} wins the game!")
                    return winner

        if not moves_available():
            print("It's a tie!")
            return "Tie"

    return None


def game_mode():
    global player_score, computer_score, is_game_on

    num_games = int(input("Enter the number of games you want to play: "))

    while num_games > 0:
        first_player = input('Who goes first? (P for Player, C for Computer): ').upper()
        player_marker = input('Select your marker (X or O): ').upper()

        if player_marker not in ['X', 'O']:
            print('Invalid marker! Please select either "X" or "O".')
            continue

        computer_marker = 'O' if player_marker == 'X' else 'X'
        level_selection = input('Select game level (E for Easy, H for Hard): ').upper()

        reset_board()

        winner = game_play(level_selection, first_player, player_marker, computer_marker)

        if winner == "Player":
            print("You win this round!")
            player_score += 1
        elif winner == "Computer":
            print("Computer wins this round!")
            computer_score += 1
        else:
            print("It's a tie!")

        print(f'\nScore: Player {player_score} - Computer {computer_score}\n')
        num_games -= 1

        if num_games == 0:
            print(f'Final Score: Player {player_score} - Computer {computer_score}')
            if play_again():
                player_score = 0
                computer_score = 0
                num_games = int(input('Enter the number of games you want to play: '))
            else:
                print('Thanks for playing!')
                break


# Helper functions to initialize board and win combinations
def initialize_possible_moves():
    return [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]


def initialize_win_combos():
    return [
        [board_list[0][0], board_list[0][1], board_list[0][2]],
        [board_list[1][0], board_list[1][1], board_list[1][2]],
        [board_list[2][0], board_list[2][1], board_list[2][2]],
        [board_list[0][0], board_list[1][0], board_list[2][0]],
        [board_list[0][1], board_list[1][1], board_list[2][1]],
        [board_list[0][2], board_list[1][2], board_list[2][2]],
        [board_list[0][0], board_list[1][1], board_list[2][2]],
        [board_list[0][2], board_list[1][1], board_list[2][0]]
    ]


def reset_board():
    global board_list, win_combos, possible_moves
    board_list = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
    possible_moves = initialize_possible_moves()
    win_combos = initialize_win_combos()


# Run the game
game_mode()
