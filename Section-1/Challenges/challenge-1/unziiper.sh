#!/bin/bash

# Function to encode the password
encode_password() {
    local plain_password=$1
    local encoding=$2
    local encoded_password=""

    case $encoding in
        base64)
            encoded_password=$(echo -n "$plain_password" | base64)
            ;;
        base32)
            encoded_password=$(echo -n "$plain_password" | base32)
            ;;
        hex)
            encoded_password=$(echo -n "$plain_password" | xxd -p)
            ;;
        plain)
            encoded_password="$plain_password"
            ;;
        *)
            echo "Unsupported encoding: $encoding"
            exit 1
            ;;
    esac

    echo "$encoded_password"
}

# Function to try all password encodings for unzip
try_unzip() {
    local input_file=$1
    local output_dir=$2
    local encoded_password=$3
    local encoding=$4

    # echo
    # echo "Trying password encoding: $encoding"
    # echo
    if [[ "$input_file" == *.zip ]]; then
        # echo "Trying to unzip $input_file with password: $encoded_password"
        unzip -P "$encoded_password" "$input_file" -d "$output_dir" 
        if [[ $? -eq 0 ]]; then
            # echo "Unzipping with $encoding Succesfull!!"
            return 0
        fi
    elif [[ "$input_file" == *.7z ]]; then
        # echo "Trying to unzip $input_file with password: $encoded_password"
        7z x -p"$encoded_password" "$input_file" -o"$output_dir" 
        if [[ $? -eq 0 ]]; then
            # echo
            # echo "Unzipping with $encoding Succesfull!!"
            # echo
            return 0
        fi
    fi


    return 1
}

# Function to decode the password
decode_password() {
    local encoded_password=$1
    local encoding=$2
    local decoded_password=""

    case $encoding in
        base64)
            decoded_password=$(echo "$encoded_password" | base64 -d 2>/dev/null)
            ;;
        base32)
            decoded_password=$(echo "$encoded_password" | base32 -d 2>/dev/null)
            ;;
        hex)
            decoded_password=$(echo "$encoded_password" | xxd -r -p 2>/dev/null)
            ;;
        plain)
            decoded_password="$encoded_password"
            ;;
        *)
            echo "Unsupported encoding: $encoding"
            exit 1
            ;;
    esac

    echo "$decoded_password"
}

# Initial variables
initial_input_file="files.zip" # or initial.7z
initial_password_file="enc_pass"
output_base_dir="unzipped_files"

mkdir -p "$output_base_dir/unzip0"



input_file="$initial_input_file"
password_file="$initial_password_file"
unzip_counter=1

# Loop to unzip the file until no .zip or .7z files are left
while true; do
    echo "--------------------------------------------------------------"
    echo "--------------------------------------------------------------"
    echo "--------------------------------------------------------------"
    echo "Iteration $unzip_counter starting"
    # echo
    # echo "File being unzipped: $input_file"
    # echo "Password file being used: $password_file"
    # echo

    output_dir="$output_base_dir/unzip$unzip_counter"
    mkdir -p "$output_dir"

    # Encode the password file into different formats for this iteration
    base64_password=$(encode_password "$(cat "$password_file")" "base64")
    base32_password=$(encode_password "$(cat "$password_file")" "base32")
    hex_password=$(encode_password "$(cat "$password_file")" "hex")
    plain_password=$(cat "$password_file")


    # echo "base64 password is: $base64_password"
    # echo "plain password is: $plain_password"
    # echo "base32 password is: $base32_password"
    # echo "hex password is: $hex_password"
    # echo


    
    # Try to unzip with all password encodings
    if ! try_unzip "$input_file" "$output_dir" "$base64_password" "base64"; then
        # echo "Failed to unzip $input_file with base64"
        if ! try_unzip "$input_file" "$output_dir" "$base32_password" "base32"; then
            # echo "Failed to unzip $input_file with base32"
            if ! try_unzip "$input_file" "$output_dir" "$hex_password" "hex"; then
                # echo "Failed to unzip $input_file with hex"
                if ! try_unzip "$input_file" "$output_dir" "$plain_password" "plain"; then
                    # echo "Failed to unzip $input_file with plain"
                    # echo
                    # echo "Failed to unzip $input_file with any encoding"
                    exit 1
                fi
            fi
        fi
    fi

    # echo
    # echo "Tried all unzipping and succeeded"
    
    # Move the used files back to their respective directories
    originalcounter=$((unzip_counter-1))
    rm "$input_file" 
    mv "$password_file" "$output_base_dir/unzip$originalcounter"


    # Prepare for the next iteration
    new_password_file=$(find "$output_dir" -type f ! -name "*.*" | head -n 1)
    input_file=$(find "$output_dir" -type f -name "*.zip" -o -name "*.7z" | head -n 1)

    if [[ -z "$new_password_file" || -z "$input_file" ]]; then
        echo "No more zip or 7z files found or password file missing"
        break
    fi

    # Move the new zip/7z file and password file to the current directory
    cp "$input_file" "."
    cp "$new_password_file" "."

    # echo 
    # echo "--------------------------------------------------------------"
    # ls -R
    # echo "--------------------------------------------------------------"
    # echo 

    # Update the password file for the next iteration
    password_file=$(basename "$new_password_file")

    echo "Iteration $unzip_counter over"

    unzip_counter=$((unzip_counter + 1))


done

echo "Successfully unzipped all files"
