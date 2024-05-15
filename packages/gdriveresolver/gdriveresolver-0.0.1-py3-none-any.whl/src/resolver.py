import time
from pathlib import Path
from typing import Optional

from .system_operations import get_operating_system, locate_google_drive


class GoogleDriveResolver:
    def __init__(self, max_depth: int = 6, max_workers: int = 5):
        self.os_type = get_operating_system()
        self.drive_path = locate_google_drive(self.os_type, max_depth, max_workers)

    def resolve(self, relative_path: str) -> Optional[Path]:
        """
        Resolve the absolute path of a file given its relative path in Google Drive.

        Parameters:
            relative_path (str): The relative path within Google Drive.

        Returns:
            Optional[Path]: The absolute path if found, else None.
        """
        absolute_path = self.drive_path / self.os_type.sanitize_path(relative_path)
        return absolute_path if absolute_path.exists() else None
