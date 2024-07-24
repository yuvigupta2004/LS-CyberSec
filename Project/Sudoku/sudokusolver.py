import copy



def find_empty_location(grid):
    for i in range(81):
        if grid[i] == 0:
            return i
    return None

def is_safe(grid, index, num):
    row = index // 9
    col = index % 9
    
    # Check if the number is not repeated in the row
    if num in grid[row*9:row*9+9]:
        return False

    # Check if the number is not repeated in the column
    for i in range(9):
        if grid[col + 9*i] == num:
            return False

    # Check if the number is not repeated in the 3x3 box
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[(start_row + i) * 9 + (start_col + j)] == num:
                return False

    return True

def solve_sudoku(grid):
    empty_location = find_empty_location(grid)
    if not empty_location:
        return True  # Sudoku is solved

    index = empty_location

    for num in range(1, 10):
        if is_safe(grid, index, num):
            grid[index] = num

            if solve_sudoku(grid):
                return True

            grid[index] = 0  # Undo the move

    return False

def Get_List_Of_Moves(original):
    
    list=[]
    unsolved = copy.deepcopy(original)
    solve_sudoku(original)
    
    for i in range(81):
        
        if unsolved[i]==0:
            ansstr=""
            row=i//9
            column=i%9
            num=original[i]
            ansstr=str(row)+" "+str(column)+" "+str(num)
            list.append(ansstr)
            
        
    return list

    
  
# sudoku_list = [
#     5, 3, 0, 0, 7, 0, 0, 0, 0,
#     6, 0, 0, 1, 9, 5, 0, 0, 0,
#     0, 9, 8, 0, 0, 0, 0, 6, 0,
#     8, 0, 0, 0, 6, 0, 0, 0, 3,
#     4, 0, 0, 8, 0, 3, 0, 0, 1,
#     7, 0, 0, 0, 2, 0, 0, 0, 6,
#     0, 6, 0, 0, 0, 0, 2, 8, 0,
#     0, 0, 0, 4, 1, 9, 0, 0, 5,
#     0, 0, 0, 0, 8, 0, 0, 7, 9
# ]

# original_sudoku=copy.deepcopy(sudoku_list)
# solve_sudoku(sudoku_list)
# print(sudoku_list)
# print(original_sudoku)

# print(Get_List_Of_Moves(original_sudoku))
