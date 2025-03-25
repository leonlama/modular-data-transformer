import csv

def create_test_csv(filename="test_data.csv"):
    # Sample header and data rows
    header = ["Name", "Age", "Department"]
    data = [
        ["Alice", "30", "Engineering"],
        ["Bob", "25", "Marketing"],
        ["Charlie", "35", "Finance"],
        ["Diana", "28", "Sales"]
    ]
    
    # Open the file in write mode and create a CSV writer
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(data)
    print(f"{filename} has been created!")

if __name__ == "__main__":
    create_test_csv()

