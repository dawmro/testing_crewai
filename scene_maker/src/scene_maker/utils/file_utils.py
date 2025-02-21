import json


def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        data = json.load(file)
        return data


def read_file(filename):
    with open(filename, "r", encoding='utf-8') as fp:
        file_content = fp.read()
        return file_content
    

def write_file(file_content, filename):
    try:
        with open(filename, "w", encoding='utf-8') as fp:
            fp.write(file_content)
        return True
    except Exception as e:
        print(f"Error writing file: {e}")
        return False


