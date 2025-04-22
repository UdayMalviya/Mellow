
import pandas as pd
import requests
import json

# Base URL for the API endpoint
BASE_URL = "http://localhost:8000"  # Change if needed

def get_datasets():
    """
    Fetches a list of available datasets from the backend.

    Returns:
        list: A list of dictionaries representing the datasets.
    """
    try:
        response = requests.get(f"{BASE_URL}/datasets/")
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except Exception as e:
        print(f"An error occurred while fetching datasets: {e}")
        return []

def upload_file(name, version_name, uploaded_file):
    """
    Uploads a file to the specified dataset.

    Args:
        name (str): The name of the dataset.
        version_name (str): The name of the version being uploaded.
        uploaded_file (Streamlit FileUploader object): The file to be uploaded.

    Returns:
        tuple: A boolean indicating success/failure and the DataFrame if successful.
    """
    try:
        # Determine the file type and read it into a DataFrame
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            return False, None

        # Generate metadata summary
        num_rows, num_columns = df.shape
        preprocessing_summary = {
            "filename": uploaded_file.name,
            "columns": df.columns.tolist(),
            "num_rows": num_rows,
            "num_columns": num_columns
        }

        # Check if the dataset already exists
        existing_datasets = get_datasets()
        dataset = next((d for d in existing_datasets if d["name"] == name), None)

        if dataset:
            dataset_id = dataset["id"]
        else:
            # Create a new dataset
            payload = {
                "name": name,
                "description": "Uploaded via Streamlit",
                "created_by": "streamlit_user"
            }
            res = requests.post(f"{BASE_URL}/datasets/", json=payload)
            if res.status_code not in [200, 201]:
                return False, None
            dataset_id = res.json()["id"]

        # Prepare and send the file
        uploaded_file.seek(0)  # Reset file pointer
        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
        data = {
            "version": version_name,
            "status": "uploaded",
            "preprocessing_summary": json.dumps(preprocessing_summary),
            "num_rows": num_rows,
            "num_columns": num_columns
        }
        version_res = requests.post(f"{BASE_URL}/versions/{dataset_id}", data=data, files=files)

        if version_res.status_code in [200, 201]:
            return True, df
        else:
            return False, None

    except Exception as e:
        print(f"An error occurred while uploading the file: {e}")
        return False, None

def get_versions(dataset_id: int):
    """
    Fetches a list of versions for a given dataset ID.

    Args:
        dataset_id (int): The ID of the dataset.

    Returns:
        list: A list of dictionaries representing the versions.
    """
    url = f"{BASE_URL}/versions/{dataset_id}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch versions: {response.text}")

    return response.json()  # List of versions

def clean_with_ai(version_id: str):
    """
    Cleans the dataset associated with the given version ID using the AI service.

    Args:
        version_id (str): The ID of the version to be cleaned.

    Returns:
        dict: The details of the cleaned version if successful, otherwise None.
    """
    try:
        response = requests.post(f"{BASE_URL}/versions/{version_id}/clean-with-ai")
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"An error occurred while cleaning the dataset: {e}")
       

    return None



