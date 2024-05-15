# import configparser
# import json
# import mimetypes
# import os
# from multiprocessing.pool import ThreadPool
# from pathlib import Path
# from typing import TypedDict
# from urllib.parse import urlparse

# import boto3

# from ..clone_storages import FileSystemStorage, S3Storage
# from ..utils import FileDict, batch_process, is_url

# config = configparser.ConfigParser()
# config.read("s3clone.ini")
# src_config = dict(config.items("src"))
# dest_config = dict(config.items("dest"))

# src = (
#     S3Storage(src_config)
#     if is_url(src_config["path"])
#     else FileSystemStorage(src_config)
# )
# dest = (
#     S3Storage(dest_config)
#     if is_url(dest_config["path"])
#     else FileSystemStorage(dest_config)
# )


# def create_temp_storage():
#     """
#     Create temp folder to store downloaded media for S3 -> S3 transfer
#     UUID is used so the script will not fail catastrophically if it is
#     executed multiple times simultaneously
#     """
#     from uuid import uuid4

#     uuid = uuid4()
#     temp_dir = f"clone-tmp-{uuid}"

#     # Temp storage is created in cwd to avoid interference with host system
#     cwd = os.path.dirname(os.path.realpath(__file__))
#     return FileSystemStorage({"path": os.path.join(cwd, temp_dir)})


# def clone():
#     temp_storage = None

#     # Local -> S3
#     if isinstance(src, FileSystemStorage) and isinstance(dest, S3Storage):
#         dest.ensure_exists()

#         def action(file: FileDict):
#             dest.save(file)

#     # S3 -> Local
#     elif isinstance(src, S3Storage) and isinstance(dest, FileSystemStorage):

#         def action(file: FileDict):
#             src.get(file, dest.path)

#     # S3 -> S3
#     elif isinstance(src, S3Storage) and isinstance(dest, S3Storage):
#         temp_storage = create_temp_storage()
#         dest.ensure_exists()

#         def action(file: FileDict):
#             # Save file from source bucket in temp Storage
#             temp_file_path = src.get(file, temp_storage.path)
#             file["path"] = temp_file_path

#             # Upload temp file to dest bucket
#             dest.save(file)

#             # Delete temp file
#             # This ensures that no matter how large the source bucket is, we will never
#             # run out of space (obv not in case of huge files)
#             temp_storage.delete(temp_file_path)

#     else:
#         raise Exception("One of src or dest has to be an S3 bucket")

#     # Use parallel processing to speed up cloning
#     batch_process(src.files, action)

#     # Clean up temp folder if it was created
#     if temp_storage:
#         import shutil

#         shutil.rmtree(temp_storage.path)


# clone()
