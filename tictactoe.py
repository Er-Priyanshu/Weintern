import os
import time
import math
import pyttsx3

# --- INITIALIZATION ---
def speak(text):
    """Uses pyttsx3 for offline voice synthesis."""
    print(f"AI: {text}")
    try:
        # Initialize locally for better stability in loops
        engine = pyttsx3.init()
        engine.setProperty('rate', 165)  # Speed of speech
        engine.setProperty('volume', 1.0) # Full volume
        
        engine.say(text)
        engine.runAndWait()
        
        # Free up the engine resource immediately
        engine.stop()
        del engine
    except Exception as e:
        print(f"(Voice Error: {e})")

# --- BOARD LOGIC ---
def print_board(board):
    print("\n")
    # Using a clearer grid format for the terminal
    for i in range(0, 9, 3):
        print(f"  {board[i]}  |  {board[i+1]}  |  {board[i+2]}  ")
        if i < 6:
            print("-----+-----+-----")
    print("\n")

def check_winner(board):
    win_patterns = [
        [0,1,2], [3,4,5], [6,7,8], [0,3,6], 
        [1,4,7], [2,5,8], [0,4,8], [2,4,6]
    ]
    for p in win_patterns:
        if board[p[0]] == board[p[1]] == board[p[2]] != " ":
            return board[p[0]]
    if " " not in board:
        return "Tie"
    return None

# --- MINIMAX ALGORITHM ---
def minimax(board, depth, is_maximizing):
    res = check_winner(board)
    if res == "O": return 10 - depth
    if res == "X": return depth - 10
    if res == "Tie": return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(board, depth + 1, False)
                board[i] = " "
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(board, depth + 1, True)
                board[i] = " "
                best_score = min(score, best_score)
        return best_score

def get_best_move(board):
    best_score = -math.inf
    move = -1
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(board, 0, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    return move

# --- MAIN GAME ---
def play():
    board = [" "] * 9
    speak("Hello , Are you Ready to lose . You are playing with an unbeatable AI")
    print_board(board)

    while True:
        try:
            move = int(input("Enter position (1-9): ")) - 1
            if move < 0 or move > 8 or board[move] != " ":
                speak("Invalid spot. Try again.")
                continue
        except ValueError:
            print("Please enter a valid number.")
            continue

        board[move] = "X"
        print_board(board)
        if check_winner(board): break

        speak("My turn. HMMMM  . Analyzing all possible futures.")
        time.sleep(0.5)
        ai_move = get_best_move(board)
        board[ai_move] = "O"
        
        if ai_move == 4:
            speak("I have secured the center.")
        else:
            speak("A logical move.")

        print_board(board)
        if check_winner(board): break

    result = check_winner(board)
    if result == "O":
        speak("I win. Better luck next time .")
    elif result == "Tie":
        speak("It is a draw.Nice try You are quite skilled.")
    else:
        speak("I lost. Error in my logic circuits!")

if __name__ == "__main__":
    play()