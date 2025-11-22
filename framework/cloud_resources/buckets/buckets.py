from framework.logging.logger import logger


class BucketInterface:
    types = {}

    def __init_subclass__(cls, **kwargs):
        logger.info(f"BucketInterface sub-class initialized for {cls.__name__}")
        cls.types[cls.Type] = cls

    @classmethod
    def get_bucket_class(cls, bucket_type, *args, **kwargs):
        if bucket_type not in cls.types:
            raise ValueError(f"Unsupported bucket type: {bucket_type}")
        return cls.types[bucket_type](*args, **kwargs)

    def upload_file(self, file_path: str, object_name: str):
        raise NotImplementedError("upload_file method not implemented.")

    def download_file(self, object_name: str, file_path: str):
        raise NotImplementedError("download_file method not implemented.")

    def delete_file(self, object_name: str):
        raise NotImplementedError("delete_file method not implemented.")

    def list_files(self):
        raise NotImplementedError("list_files method not implemented.")


class AzureBucket(BucketInterface):
    Type = "azure"

    def __init__(self, connection_string: str):
        from azure.storage.blob import BlobServiceClient

        self.blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )
        self.bucket_name = None  # need to set the container name

    def upload_file(self, file_path: str, object_name: str):
        container_client = self.blob_service_client.get_container_client(
            self.bucket_name
        )
        with open(file_path, "rb") as data:
            container_client.upload_blob(name=object_name, data=data)

    def download_file(self, object_name: str, file_path: str):
        container_client = self.blob_service_client.get_container_client(
            self.bucket_name
        )
        blob_client = container_client.get_blob_client(object_name)
        with open(file_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())

    def delete_file(self, object_name: str):
        container_client = self.blob_service_client.get_container_client(
            self.bucket_name
        )
        container_client.delete_blob(object_name)

    def list_files(self):
        container_client = self.blob_service_client.get_container_client(
            self.bucket_name
        )
        return [blob.name for blob in container_client.list_blobs()]
