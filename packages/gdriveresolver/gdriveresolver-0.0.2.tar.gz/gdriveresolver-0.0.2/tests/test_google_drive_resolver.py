import unittest
from unittest.mock import patch
from pathlib import Path

from src.exceptions import GDriveNotFoundError
from src.model import mac_definition, windows_definition, linux_definition
from src.resolver import GoogleDriveResolver
from src.system_operations import get_operating_system, locate_google_drive


class TestGoogleDriveResolver(unittest.TestCase):

    @patch('src.system_operations.sys.platform', 'darwin')
    def test_get_operating_system_mac(self):
        # Given: The system platform is macOS (darwin)
        os_type = get_operating_system()

        # When: Getting the operating system definition
        # Then: It should return mac_definition
        self.assertEqual(os_type, mac_definition)

    @patch('src.system_operations.sys.platform', 'win32')
    def test_get_operating_system_windows(self):
        # Given: The system platform is Windows (win32)
        os_type = get_operating_system()

        # When: Getting the operating system definition
        # Then: It should return windows_definition
        self.assertEqual(os_type, windows_definition)

    @patch('src.system_operations.sys.platform', 'linux')
    def test_get_operating_system_linux(self):
        # Given: The system platform is Linux (linux)
        os_type = get_operating_system()

        # When: Getting the operating system definition
        # Then: It should return linux_definition
        self.assertEqual(os_type, linux_definition)

    @patch('src.system_operations.Path.home')
    def test_locate_google_drive_common_location(self, mock_home):
        # Given: The home path contains a Google Drive folder
        mock_home.return_value = Path('/mock/home')
        mock_path = Path('/mock/home/Google Drive')
        os_type = mac_definition

        # When: Locating the Google Drive path
        with patch.object(Path, 'exists', return_value=True):
            drive_path = locate_google_drive(os_type, max_depth=3, max_workers=4)

            # Then: It should return the path to the Google Drive folder
            self.assertEqual(drive_path, mock_path)

    @patch('src.system_operations.os.walk')
    def test_locate_google_drive_not_found(self, mock_walk):
        # Given: The directory does not contain a Google Drive folder
        os_type = mac_definition
        mock_walk.return_value = [
            ('/mock/root', ['SomeOtherFolder'], []),
        ]

        # When: Locating the Google Drive path
        with patch.object(Path, 'exists', return_value=False):
            # Then: It should raise a GDriveNotFoundError
            with self.assertRaises(GDriveNotFoundError):
                locate_google_drive(os_type, max_depth=3, max_workers=4)

    @patch('src.system_operations.Path.exists')
    def test_resolve_existing_path(self, mock_exists):
        # Given: The relative path exists in Google Drive
        mock_exists.return_value = True
        resolver = GoogleDriveResolver(max_depth=3, max_workers=4)
        resolver.drive_path = Path('/mock/root/Google Drive')
        relative_path = 'Shared Drives/MyDir/myfile.csv'

        # When: Resolving the relative path
        resolved_path = resolver.resolve(relative_path)

        # Then: It should return the full path to the file
        self.assertEqual(resolved_path, Path('/mock/root/Google Drive/Shared Drives/MyDir/myfile.csv'))

    @patch('src.system_operations.Path.exists')
    def test_resolve_nonexistent_path(self, mock_exists):
        # Given: The relative path does not exist in Google Drive
        mock_exists.return_value = False
        resolver = GoogleDriveResolver(max_depth=3, max_workers=4)
        resolver.drive_path = Path('/mock/root/Google Drive')
        relative_path = 'Shared Drives/NonExistent'

        # When: Resolving the relative path
        resolved_path = resolver.resolve(relative_path)

        # Then: It should return None
        self.assertIsNone(resolved_path)


if __name__ == '__main__':
    unittest.main()
