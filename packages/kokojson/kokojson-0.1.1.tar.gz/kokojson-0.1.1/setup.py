from setuptools import setup, find_packages

setup(
    name="kokojson",
    version="0.1.1",
    author="kokofixcomputers",
    author_email="kokocanfixit@kokofixcomputers.serv00.net",
    description="A module for safe JSON handling in Python",
    long_description='''## A module for safe JSON handling in Python

### Example Usage:
data.json:
```json
{
  "person": {
    "name": "John Doe",
    "age": 30,
    "city": "New York"
  },
  "company": {
    "name": "Acme Inc.",
    "employees": 500
  }
}
 }
}
```
```python
import kokojson as json1

# Load the JSON data from the file
with open("data.json", "r") as file:
    data = file.read()

# Parse the JSON data using kokojson
json_data = json1.load(data)

# Access existing keys
print(json_data.get("person").get("name"))  # Output: John Doe
print(json_data.get("company").get("employees"))  # Output: 500

# Access non-existing keys (returns None instead of raising an exception)
print(json_data.get("person").get("email"))  # Output: None
print(json_data.get("company").get("website"))  # Output: None

# Provide a default value for non-existing keys
print(json_data.get("person").get("email", "No email found"))  # Output: No email found
print(json_data.get("company").get("website", "https://example.com"))  # Output: https://example.com
```
''',
    long_description_content_type="text/markdown",
    url="https://github.com/your_username/kokojson",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)