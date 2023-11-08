import json

# Python dictionary (map)
data = {
    "name": "John",
    "age": 30,
    "city": "New York"
}

# Convert dictionary to JSON string
json_data = json.dumps(data)

# Print the JSON string
print("JSON representation:")
print(json_data)

# Convert JSON string to dictionary
parsed_data = json.loads(json_data)

# Print the Python dictionary
print("Python dictionary:")
print(parsed_data)
