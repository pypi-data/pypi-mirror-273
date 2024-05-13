import os

def get_code():
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'data', 'my_code.py')
    with open(file_path, 'r') as file:
        return file.read()
