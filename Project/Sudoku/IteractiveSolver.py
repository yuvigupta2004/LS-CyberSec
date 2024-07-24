from sudokusolver import Get_List_Of_Moves
import subprocess
import re
from tqdm import tqdm

process = subprocess.Popen(["./sudoku"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
count = 0
for k in tqdm(range(840)):
    sudoku = []
    while (line := process.stdout.readline()) and len(sudoku) < 9:
        if 'Snuday' in line:
            count += 1
        line = line.strip()
        row = []
        if re.match(r"\| [0-9\.] [0-9\.] [0-9\.] \|", line):
            for char in line:
                if char == ".":
                    row.append(0)
                elif char.isdigit():
                    row.append(int(char))
            sudoku.append(row)
    
    sudokulist = []
    for row in sudoku:
        for i in row:
            sudokulist.append(int(i))
    print("hi")
    print(sudokulist)
    ans = NextStepSudokuSolver(sudokulist)
    print("bye")
    print(ans)
    process.stdin.write(ans)
    process.stdin.flush()
    
   
        
        
while (line := process.stdout.readline()):
    print(line.strip())