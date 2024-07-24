import subprocess

def check_password(executable, candidate):
    
    process = subprocess.Popen([executable], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Read the prompt from the subprocess
    result, error = process.communicate(input=candidate)
    
    output = result.strip()
    output=output.split()
    output=output[4:]
    output = ' '.join(output)
    print("Output is:",output)
    
    if output.startswith("WRONG"):
        
        if "low" in output:
            return -1
        elif "high" in output:
            return 1
    else:
        return 0
    

def binary_search(wordlist, executable):
    low = 0
    high = len(wordlist) - 1
    global count
    count+=1
    print(count)
    
    while low <= high:
        mid = (low + high) // 2
        print("Checking Passwrod:",wordlist[mid])
        result = check_password(executable, wordlist[mid])
        
        if result == 0:
            return wordlist[mid]
        elif result < 0:
            low = mid + 1
        else:
            high = mid - 1

    return None

count=0
def main():
    executable = "./bruteforcer"  # Path to your executable
    
    # Load the wordlist from the file
    with open('wordlist.txt', 'r') as file:
        wordlist = file.read().splitlines()
    
    # Sort the wordlist if it's not already sorted
    wordlist.sort()

    # Perform binary search to find the correct password
    correct_password = binary_search(wordlist, executable)
    
    if correct_password:
        print(f"The correct password is: {correct_password}")
    else:
        print("Password not found in the wordlist.")

if __name__ == "__main__":
    main()

