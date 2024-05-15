# Kudra Cloud Client

### Overview :

`kudra-cloud-client` is a Python package designed to simplify the process of uploading and analyzing documents using the Kudra Cloud service [kudra.ai](https://kudra.ai/) .

## Installation

Install the package using `pip`: 

```bash
pip install KudraCloudClient
```

## Usage

### Example :
```python
from kudra_cloud_client import KudraCloudClient

# Initialize KudraCloudClient with your authentication token
kudraCloud = KudraCloudClient(token="YOUR_AUTHENTICATION_TOKEN")

# Specify the directory containing the files to be uploaded
files_dir = "path/to/your/files"

# Specify the project run ID
project_run_id = "your_project_run_id"

# Analyze documents and get the result
result = kudraCloud.analyze_documents(files_dir=files_dir, project_run_id=project_run_id)

# Log the result or process it as needed
print(result)
```
## Requirements

- Python 3.8+

## Error Handling
If an error occurs during the upload or analysis process, an exception will be raised, and details will be logged.

## License
This project is licensed under the MIT License - see the ```LICENSE.txt``` file for details.
