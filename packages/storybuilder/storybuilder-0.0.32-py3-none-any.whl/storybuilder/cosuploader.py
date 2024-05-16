from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos import CosServiceError
from qcloud_cos import CosClientError

import os
import hashlib


class CosUploader:
    def __init__(
        self,
        service_root,
        cos_region,
        cos_secret_id,
        cos_secret_key,
        cos_bucket,
        cos_token=None,
        cos_scheme="https",
    ):
        self.service_root = service_root
        self._config = CosConfig(
            Region=cos_region,
            SecretId=cos_secret_id,
            SecretKey=cos_secret_key,
            Token=cos_token,
            Scheme=cos_scheme,
        )
        self._client = CosS3Client(self._config)
        self._bucket = cos_bucket

    def calculate_file_hash(self, file_path):
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def get_file_name(self, file_path):
        filename, file_extension = os.path.splitext(os.path.basename(file_path))
        return filename + "_" + self.calculate_file_hash(file_path) + file_extension

    def local2cos(self, local_path, storyId, target_relative_path="test"):
        if target_relative_path is None:
            target_relative_path = ""
        elif len(target_relative_path) > 0:
            target_relative_path = (
                target_relative_path
                if target_relative_path[0] != "/"
                else target_relative_path[1:]
            )
        try:
            filename = os.path.join(
                target_relative_path,
                storyId,
                self.get_file_name(local_path),
            )
        except:
            print("file not found:", local_path)
        response = self._client.upload_file(
            Bucket=self._bucket, LocalFilePath=local_path, Key=filename
        )
        return "/"+filename
