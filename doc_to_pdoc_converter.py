import json

# Specify the path to your JSON file
json_file_path = r"C:\Users\prath\Desktop\Assignment 7 new\file_to_urldict.json"

# Open the JSON file
with open(json_file_path, 'r') as file:
    # Load the JSON content into a Python dictionary
    data = json.load(file)

# Convert all keys by attaching 'p' in front of each key
modified_dict = {f'p{key}': value for key, value in data.items()}

print(modified_dict)
print(type(modified_dict))

# Specify the path where you want to save the JSON file
json_file_path = r'C:\Users\prath\Desktop\Assignment 7 new\pdoc_to_url_index.json'

# Save the dictionary as a JSON file
with open(json_file_path, 'w') as json_file:
    json.dump(modified_dict, json_file, indent=4)

print(f'The dictionary has been saved as {json_file_path}')
