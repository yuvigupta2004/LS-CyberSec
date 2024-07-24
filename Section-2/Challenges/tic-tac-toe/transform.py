import json

# Function to transform the data
def transform_data(input_data):
    output_data = {}
    for key, value in input_data.items():
        # Find the key in the dictionary with a value of 1
        new_value = [k for k, v in value.items() if v == 1]
        if new_value:
            output_data[key] = new_value[0]
    return output_data

# Read the JSON file
with open('policy_x.json', 'r') as f:
    data = json.load(f)

# Transform the data
transformed_data = transform_data(data)

# Write the transformed data to a new JSON file
with open('output.json', 'w') as f:
    json.dump(transformed_data, f, indent=4)

print("Transformation complete. Check output.json for the result.")
