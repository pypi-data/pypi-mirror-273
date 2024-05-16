import re
from pathlib import Path

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

from sona.settings import settings

from .base import SourceBase


class AzureBlobSource(SourceBase):
    setting = settings.SONA_STORAGE_AZURE_BLOB_SETTING

    @classmethod
    def get_client(cls):
        configs = cls.setting or {}
        return BlobServiceClient(credential=DefaultAzureCredential(), **configs)

    @classmethod
    def download(cls, file):
        match = re.match(r"[Ss]3://([-_\w]+)/(.+)", file.path)
        bucket = match.group(1)
        obj_key = match.group(2)

        filename = Path(obj_key).name
        tmp_path = cls.tmp_dir / filename

        container_client = cls.get_client().get_container_client(container=bucket)
        with open(file=tmp_path, mode="wb") as download_file:
            download_file.write(container_client.download_blob(obj_key).readall())
        return file.mutate(path=str(tmp_path))

    @classmethod
    def verify(cls, file):
        return (
            file.path and file.path.startswith("s3://") or file.path.startswith("S3://")
        )
