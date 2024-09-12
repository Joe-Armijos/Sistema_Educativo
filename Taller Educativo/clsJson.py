import json
import os

class JsonFile:
    def __init__(self, file_path):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                json.dump([], file)

    def read(self):
        with open(self.file_path, 'r') as file:
            return json.load(file)

    def write(self, data):
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=2)

    def add(self, item):
        data = self.read()
        data.append(item)
        self.write(data)

    def update(self, identifier_key, identifier_value, new_data):
        data = self.read()
        updated = False
        for index, item in enumerate(data):
            if item.get(identifier_key) == identifier_value:
                data[index].update(new_data)
                updated = True
                break
        if updated:
            self.write(data)
        else:
            raise ValueError(f"Item with {identifier_key} '{identifier_value}' not found.")

    def delete(self, identifier_key, identifier_value):
        data = self.read()
        new_data = [item for item in data if item.get(identifier_key) != identifier_value]
        if len(new_data) == len(data):
            raise ValueError(f"Item with {identifier_key} '{identifier_value}' not found.")
        self.write(new_data)

    def find(self, identifier_key, identifier_value):
        data = self.read()
        for item in data:
            if item.get(identifier_key) == identifier_value:
                return item
        return None
