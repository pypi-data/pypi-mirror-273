from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

from sona.settings import settings

from .base import StorageBase


class AzureBlobStorage(StorageBase):
    def __init__(
        self,
        bucket=settings.SONA_STORAGE_AZURE_BLOB_CONTAINER,
        configs=settings.SONA_STORAGE_AZURE_BLOB_SETTING,
    ):
        super().__init__()
        self.bucket = bucket
        self.configs = configs

    @property
    def client(self):
        configs = self.configs or {}
        return BlobServiceClient(credential=DefaultAzureCredential(), **configs)

    def on_push(self, file, remote_path):
        blob = self.client.get_blob_client(container=self.bucket, blob=remote_path)
        with open(file=file.path, mode="rb") as data:
            blob.upload_blob(data)
        return file.mutate(path=f"S3://{self.bucket}/{remote_path}")
