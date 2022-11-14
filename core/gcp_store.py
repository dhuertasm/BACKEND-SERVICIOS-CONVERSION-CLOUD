from google.cloud import storage
from constans import BUCKET_KEY_GCP, UPLOAD_FOLDER


class GCP:

    def gcp(self):
        bucket_name = "nube-media-files"
        storage_client = storage.Client.from_service_account_json(
            f'{BUCKET_KEY_GCP}/flask-test-366421-83ae86406dca.json')
        return storage_client.bucket(bucket_name)

    def upload_store_gcp(self, file, file_name):
        """Write and read a blob from GCS using file-like IO"""

        # file_open = open(file, 'rb')
        audio_bytes = file.read()

        blob_name = f"mediafiles/{file_name}"

        blob = self.gcp().blob(blob_name)

        blob.upload_from_string(
            audio_bytes
        )

    def download_store_gcp(self, file_name):
        """Write and read a blob from GCS using file-like IO"""

        # file_open = open(file, 'rb')

        blob_name = f"mediafiles/{file_name}"

        blob = self.gcp().blob(blob_name)

        blob.download_to_filename(f"{UPLOAD_FOLDER}/{file_name}")
        return True

    def download_store_bytes_gcp(self, file_name):
        """Write and read a blob from GCS using file-like IO"""

        # file_open = open(file, 'rb')

        blob_name = f"mediafiles/{file_name}"

        blob = self.gcp().blob(blob_name)

        return blob.download_as_bytes(f"{UPLOAD_FOLDER}/{file_name}")
