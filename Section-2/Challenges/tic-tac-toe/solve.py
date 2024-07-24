import json
import subprocess

# Path to the executable
executable = './ttt'

# Load the JSON data
with open('./output.json', 'r') as f:
    data = json.load(f)


'''
DATA IS A DICTIONARY WITH HISTORY AS KEY AND NEXT POSITION AS VALUE
0 1 2
3 4 5
6 7 8
'''


# Convert the next positions in the JSON data to "row,column" format
for key in data:
    nextpos = int(data[key])
    columnnumber = nextpos % 3
    rownumber = (nextpos - columnnumber) // 3
    data[key] = f"{rownumber},{columnnumber}"

game_number = 1
history = ""
historylist = [0] * 9
newhistorylist = [0] * 9
rownum = 0

# Run the executable and capture its output
process = subprocess.Popen(executable, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True)

while process.poll() is None:  # Check if the process is running
    line = process.stdout.readline().strip()
    if not line:
        continue
    
    # Ignore lines containing "bot"
    if "bot" in line:
        continue
    
    # Capture game number
    if "Game" in line:
        game_number = int(line.split()[1][1:-5])
        history = ""
        historylist = [0] * 9
        newhistorylist = [0] * 9
        rownum = 0
        print("Game number is:", game_number)
        continue
    
    # Process board lines
    if "Enter" not in line:
        print(line)
        for index in range(len(line)):
            char = line[index]
            if char in ["x", "o"]:
                
                squarenumber=rownum * 3 + index // 2
                
                
                newhistorylist[squarenumber]=1
                
        
        rownum += 1
        
        if rownum == 3:
            
            # if "0" in history:
            #     print(history)
            #     print(newhistorylist)
            #     print(historylist)
                
            #     exit()
            
            for i in range(9):
                if historylist[i] != newhistorylist[i]:
                    print("Opponent Move:", i)
                    history += str(i)
                    historylist[i]=1
                    
            rownum = 0
            newhistorylist = [0] * 9
    
    # Handle the "Enter" prompt
    if "Enter" in line:
        print(line)
        newmove = data[history]
        rownumber, columnnumber = map(int, newmove.split(','))
        squarenumber = rownumber * 3 + columnnumber
        
        # if squarenumber not in historylist:
        
        historylist[squarenumber]=1
       
        history += str(squarenumber)
        
        print("My move:", squarenumber)
        # print(history)
        # print(newhistorylist)
        # print(historylist)
        
        process.stdin.write(f"{newmove}\n")
        process.stdin.flush()  # Ensure input is processed
        

# Close the process if still running
if process.poll() is None:
    process.terminate()
