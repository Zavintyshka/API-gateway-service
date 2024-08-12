import os
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from fastapi import Request, Response


class CacheValidator:
    def __init__(self, request: Request, file_path: Path):
        self.__request = request
        self.file_etag = self.__get_etag(file_path)
        self.t_format = "%a, %d %b %Y %H:%M:%S %Z"
        self.last_modified_date, self.last_modified_date_str = self.__get_last_modified_date(file_path)

    @staticmethod
    def __get_etag(file_path: Path) -> str:
        file_stat = os.stat(file_path)
        etag = hashlib.md5(f"{file_stat.st_mtime}_{file_stat.st_size}".encode()).hexdigest()
        return etag

    def __get_last_modified_date(self, file_path: Path):
        last_modified_timestamp = int(os.stat(file_path).st_mtime)
        last_modified_date = datetime.fromtimestamp(last_modified_timestamp, tz=timezone.utc)
        return last_modified_date, last_modified_date.strftime(self.t_format)

    def __etag_validation(self) -> bool:
        client_etag = self.__request.headers.get("If-None-Match")
        return client_etag and self.file_etag == client_etag

    def __time_validation(self) -> bool:
        if_modified_since_header = self.__request.headers.get("If-Modified-Since")
        if not if_modified_since_header:
            return False
        if_modified_since_date = datetime.strptime(if_modified_since_header, self.t_format).replace(
            tzinfo=timezone.utc)
        return self.last_modified_date <= if_modified_since_date

    def validate_cache_headers(self):
        return self.__etag_validation() or self.__time_validation()

    def get_304_response(self):
        headers = {"ETag": self.file_etag, "Last-Modified": self.last_modified_date_str}
        return Response(status_code=304, headers=headers)
