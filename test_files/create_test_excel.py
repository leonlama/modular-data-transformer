import pandas as pd

def create_test_excel(filename="test_data.xlsx"):
    # Sample data
    data = {
        "Name": ["Alice", "Bob", "Charlie", "Diana"],
        "Age": [30, 25, 35, 28],
        "Department": ["Engineering", "Marketing", "Finance", "Sales"]
    }
    df = pd.DataFrame(data)

    # Write DataFrame to Excel
    df.to_excel(filename, index=False)
    print(f"{filename} created successfully.")

if __name__ == "__main__":
    create_test_excel()

