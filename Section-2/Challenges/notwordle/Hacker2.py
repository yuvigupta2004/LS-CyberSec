import subprocess
import string


def check_password(executable, candidate):
    
    process = subprocess.Popen([executable], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    global count
    # Read the prompt from the subprocess
    result, error = process.communicate(input=candidate)
    
    output = result.strip()
    output=output.split()
    output=output[13:]
    output = ' '.join(output)
    print("Output is:",output)
    
    if output.startswith(str(count+1)):
        count+=1
        return 1
    else:
        return 0
    

count=0

executable1 = "./notwordle"  # Path to your executable
alphanumeric_and_underscore = list(string.ascii_letters + string.digits + '_')
password=""


while count<30:
    ogpass=password
    for i in alphanumeric_and_underscore:
        password=ogpass
        password+=i
        print("checking password:",password)
        if check_password(executable1, password):
            print("currentpassword:",password)
            break
  
        
        
