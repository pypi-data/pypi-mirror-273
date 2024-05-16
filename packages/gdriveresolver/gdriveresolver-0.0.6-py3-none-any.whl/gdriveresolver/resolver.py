from pathlib import Path
from typing import Optional

from .model import OSDefinition
from .system_operations import get_operating_system, locate_google_drive


class GDriveResolver:
    def __init__(self, max_depth: int = 6, max_workers: int = 5):
        self.os_type: OSDefinition = get_operating_system()
        self.drive_path: Optional[Path] = locate_google_drive(self.os_type, max_depth, max_workers)

    def resolve(self, path_to_resolve: str, must_resolve: bool = True) -> Optional[str]:
        """
        Resolve the absolute path of a file given its relative path in Google Drive.

        Parameters:
            path_to_resolve (str): The relative path within Google Drive.
            must_resolve (bool): Whether to raise an error if the file is not found.

        Returns:
            Optional[str]: The absolute path if found, else None.
        """
        as_path = Path(path_to_resolve)

        # Case 1: If Google Drive path is resolved, check path relative to Google Drive
        if self.drive_path:
            sanitized_path = self.os_type.sanitize_path(path_to_resolve)
            absolute_path = self.drive_path / sanitized_path
            if absolute_path.exists():
                return str(absolute_path)
            else:
                return _terminate(must_resolve)

        # Case 2: Google Drive path is not resolved, check against absolute path
        if as_path.is_absolute():
            if as_path.exists():
                return str(as_path)
            else:
                return _terminate(must_resolve)

        # Case 3: If Google Drive path is not resolved, check path relative to root search paths
        for root in self.os_type.root_search_paths:
            potential_path = root / as_path
            if potential_path.exists():
                return str(potential_path)

        return _terminate(must_resolve)


def _terminate(must_resolve: bool) -> None:
    if must_resolve:
        raise FileNotFoundError("File not found.")
    print("File not found.")
    return None
