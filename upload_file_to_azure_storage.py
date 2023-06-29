import os
import argparse
from azure.storage.blob import BlobServiceClient


def save_file_to_azure(
    file_path,
    azure_storage_account_name,
    azure_storage_account_key,
    azure_container_name,
):
    # Connect to Azure Blob Storage and upload the image
    blob_service_client = BlobServiceClient(
        account_url=f"https://{azure_storage_account_name}.blob.core.windows.net",
        credential=azure_storage_account_key,
    )
    container_client = blob_service_client.get_container_client(azure_container_name)

    with open(file_path, "rb") as data:
        blob_client = container_client.get_blob_client(os.path.basename(file_path))
        blob_client.upload_blob(data, overwrite=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload an image to Azure storage.")
    parser.add_argument("--file_path", required=True, help="Full path to zip file")
    parser.add_argument(
        "--azure_storage_account_name", required=True, help="Azure storage account name"
    )
    parser.add_argument(
        "--azure_storage_account_key", required=True, help="Azure storage account key"
    )
    parser.add_argument(
        "--azure_container_name", required=True, help="Azure container name"
    )

    args = parser.parse_args()

    save_file_to_azure(
        args.file_path,
        args.azure_storage_account_name,
        args.azure_storage_account_key,
        args.azure_container_name,
    )
