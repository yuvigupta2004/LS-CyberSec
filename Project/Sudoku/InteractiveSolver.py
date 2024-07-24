import subprocess
from sudokusolver import Get_List_Of_Moves
import re
from tqdm import tqdm


def getlistfromgrid(sudoku):
    sudokulist=[]
    for row in sudoku:
        for i in row:
            sudokulist.append(int(i))

    return sudokulist


process = subprocess.Popen(["./sudoku"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
count = 0
for k in range(840):
    sudoku = []
    while (line := process.stdout.readline().decode()) and len(sudoku) < 9:
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
            
    sudokulist = getlistfromgrid(sudoku)     
    listofmoves=Get_List_Of_Moves(sudokulist)
    
    for i in range(len(listofmoves)):
        answer = listofmoves[i]+"\n"
        process.stdin.write(answer.encode())
        process.stdin.flush()
        if i != len(listofmoves) - 1:
            for i in range(14):
                line = process.stdout.readline()
while (line := process.stdout.readline()):
    print(line.decode().strip())