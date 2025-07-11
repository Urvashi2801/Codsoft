import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Tic Tac Toe: You (X) vs AI (O)")
root.resizable(False, False)

board = [["" for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]

# Check winner
def check_winner():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "":
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]
    return None

def check_draw():
    for row in board:
        if "" in row:
            return False
    return True

# Minimax AI
def minimax(is_maximizing):
    winner = check_winner()
    if winner == "O":
        return 1
    elif winner == "X":
        return -1
    elif check_draw():
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "O"
                    score = minimax(False)
                    board[i][j] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "X"
                    score = minimax(True)
                    board[i][j] = ""
                    best_score = min(score, best_score)
        return best_score

# Best move for AI
def computer_move():
    best_score = -float('inf')
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                board[i][j] = "O"
                score = minimax(False)
                board[i][j] = ""
                if score > best_score:
                    best_score = score
                    move = (i, j)

    if move:
        row, col = move
        board[row][col] = "O"
        buttons[row][col].config(text="O", state="disabled")

    winner = check_winner()
    if winner:
        messagebox.showinfo("Game Over", f"{'You' if winner == 'X' else 'Computer'} wins!")
        reset_game()
    elif check_draw():
        messagebox.showinfo("Game Over", "It's a draw!")
        reset_game()

# User click handler
def button_click(row, col):
    if board[row][col] == "":
        board[row][col] = "X"
        buttons[row][col].config(text="X", state="disabled")

        winner = check_winner()
        if winner:
            messagebox.showinfo("Game Over", "You win!")
            reset_game()
        elif check_draw():
            messagebox.showinfo("Game Over", "It's a draw!")
            reset_game()
        else:
            root.after(300, computer_move)

# Reset the game
def reset_game():
    global board
    board = [["" for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text="", state="normal")

# Create the board buttons
for i in range(3):
    for j in range(3):
        btn = tk.Button(root, text="", font=('Helvetica', 24), width=5, height=2,
                        command=lambda r=i, c=j: button_click(r, c))
        btn.grid(row=i, column=j)
        buttons[i][j] = btn

# Reset Button
reset_btn = tk.Button(root, text="Reset", font=('Helvetica', 14), command=reset_game)
reset_btn.grid(row=3, column=0, columnspan=3, sticky="nsew")

root.mainloop()
