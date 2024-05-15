import json

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: The file at {file_path} does not exist.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file at {file_path} is not a valid JSON.")
        return None

def write_results_to_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)