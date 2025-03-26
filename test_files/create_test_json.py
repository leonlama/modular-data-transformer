import json

def create_test_json(filename="test_data.json"):
    # Sample data: a list of dictionaries
    data = [
        {"Name": "Alice", "Age": 30, "Department": "Engineering"},
        {"Name": "Bob", "Age": 25, "Department": "Marketing"},
        {"Name": "Charlie", "Age": 35, "Department": "Finance"},
        {"Name": "Diana", "Age": 28, "Department": "Sales"}
    ]
    
    # Write the JSON data to file with indentation for readability
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"{filename} has been created!")

if __name__ == "__main__":
    create_test_json()

