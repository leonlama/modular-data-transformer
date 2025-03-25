def create_test_xml(filename="test_data.xml"):
    # A simple XML structure
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<root>
    <employee>
        <name>Alice</name>
        <age>30</age>
        <department>Engineering</department>
    </employee>
    <employee>
        <name>Bob</name>
        <age>25</age>
        <department>Marketing</department>
    </employee>
    <employee>
        <name>Charlie</name>
        <age>35</age>
        <department>Finance</department>
    </employee>
    <employee>
        <name>Diana</name>
        <age>28</age>
        <department>Sales</department>
    </employee>
</root>
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(xml_content)
    print(f"{filename} created successfully.")

if __name__ == "__main__":
    create_test_xml()

