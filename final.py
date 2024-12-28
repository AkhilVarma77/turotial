
#---------------------------------------------------------------------------------------------------------------------
import tkinter as tk
import copy
import time

canvas = None
board = [
    [-1, -1, 1, 1, 1, -1, -1],
    [-1, -1, 1, 1, 1, -1, -1],
    [ 1,  1, 1, 1, 1,  1,  1],
    [ 1,  1, 1, 0, 1,  1,  1],
    [ 1,  1, 1, 1, 1,  1,  1],
    [-1, -1, 1, 1, 1, -1, -1],
    [-1, -1, 1, 1, 1, -1, -1]
]
solution_steps = []
visited_states = set()

def initialize_gui():
    
    global canvas
    root = tk.Tk()
    root.title("Peg Solitaire Solver (DFS & Goal-Based Agent)")
    canvas = tk.Canvas(root, width=350, height=350, bg="white")
    canvas.pack()
    return root

def draw_board(board):
    canvas.delete("all")
    cell_size = 50
    for i in range(7):
        for j in range(7):
            x1, y1 = i * cell_size, j * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size

        
            if board[i][j] == -1:  
                canvas.create_rectangle(x1, y1, x2, y2, fill="gray", outline="black")
            elif board[i][j] == 1:  
                canvas.create_oval(x1 + 10, y1 + 10, x2 - 10, y2 - 10, fill="red", outline="black")
            elif board[i][j] == 0: 
                canvas.create_oval(x1 + 10, y1 + 10, x2 - 10, y2 - 10, fill="white", outline="black")


#-------------------------------------------------------------------------------------------------------------------

#depth first search
#------------------------------------------------------------------------------------------------------------------
def solve_with_dfs(board, path):
    
    global solution_steps, visited_states

    if is_solved(board):
        solution_steps.extend(path + [copy.deepcopy(board)])
        return True

    board_key = board_to_key(board)
    if board_key in visited_states:
        return False
    visited_states.add(board_key)

    for next_board in get_next_boards(board):
        if solve_with_dfs(next_board, path + [copy.deepcopy(board)]):
            return True

    return False

# ----------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------
# goal based agent
def solve_with_goal_based_agent(board):
    global solution_steps, visited_states

    if is_solved(board):
        solution_steps.append(copy.deepcopy(board))
        return True

    board_key = board_to_key(board)
    if board_key in visited_states:
        return False
    visited_states.add(board_key)
    
    for next_board in get_next_boards(board):
        if solve_with_goal_based_agent(next_board):
            solution_steps.append(copy.deepcopy(next_board))
            return True

    return False

def get_next_boards(board):
    next_boards = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  

    for i in range(7):
        for j in range(7):
            if board[i][j] == 1:  
                for dx, dy in directions:
                    x1, y1 = i + dx, j + dy
                    x2, y2 = i + 2 * dx, j + 2 * dy

                    if is_valid_move(board, i, j, x1, y1, x2, y2):
                        new_board = copy.deepcopy(board)
                        new_board[i][j] = 0
                        new_board[x1][y1] = 0
                        new_board[x2][y2] = 1
                        next_boards.append(new_board)
    return next_boards
#------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------
def is_valid_move(board, x, y, x1, y1, x2, y2):
    return (0 <= x2 < 7 and 0 <= y2 < 7 and
            board[x][y] == 1 and board[x1][y1] == 1 and board[x2][y2] == 0)

def is_solved(board):
    return sum(row.count(1) for row in board) == 1

def board_to_key(board):
    return tuple(tuple(row) for row in board)

def visualize_solution(root):
    global board
    for step in solution_steps:
        board = step
        draw_board(board)
        root.update()
        time.sleep(0.5)

def main():
    global solution_steps, visited_states

    root = initialize_gui()

    # For DFS:
    solve_with_dfs(board, [])
    # Or for Goal-Based Agent:
    #solve_with_goal_based_agent(board)

    visualize_solution(root)

    root.mainloop()

if __name__ == "__main__":
    main()
# _---------------------------------------------------------------------------------------------------------------