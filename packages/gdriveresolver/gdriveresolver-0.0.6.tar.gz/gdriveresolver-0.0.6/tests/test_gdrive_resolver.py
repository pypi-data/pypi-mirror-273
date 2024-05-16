import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from gdriveresolver.resolver import GDriveResolver


class TestGDriveResolver(unittest.TestCase):

    def setUp(self):
        self.resolver = GDriveResolver()

    @patch('gdriveresolver.system_operations.get_operating_system')
    def test_resolve_relative_path(self, mock_get_os):
        """
        Given a relative path within Google Drive
        When the Google Drive path is resolved
        Then it should return the absolute path within Google Drive
        """
        # Given
        mock_os = MagicMock()
        mock_get_os.return_value = mock_os
        self.resolver.drive_path = Path('/mock/google_drive')
        mock_os.sanitize_path.return_value = 'relative/path/to/file.txt'

        path = 'relative/path/to/file.txt'
        expected_path = '/mock/google_drive/relative/path/to/file.txt'

        # When
        with patch.object(Path, 'exists', return_value=True):
            result = self.resolver.resolve(path)

        # Then
        assert result == expected_path

    @patch('gdriveresolver.resolver.locate_google_drive')
    @patch('gdriveresolver.resolver.get_operating_system')
    def test_resolve_absolute_path(self, mock_get_os, mock_locate_drive):
        """
        Given an absolute path
        When the Google Drive path is not resolved
        Then it should return the absolute path directly
        """
        # Given
        mock_get_os.return_value = MagicMock()
        mock_locate_drive.return_value = None

        path = '/absolute/path/to/file.txt'
        expected_path = '/absolute/path/to/file.txt'

        # When
        with patch.object(Path, 'is_absolute', return_value=True):
            with patch.object(Path, 'exists', return_value=True):
                result = self.resolver.resolve(path)

        # Then
        assert result == expected_path

    @patch('gdriveresolver.resolver.get_operating_system')
    def test_resolve_relative_to_root_search_paths(self, mock_get_os):
        """
        Given a relative path
        When the Google Drive path is not resolved
        Then it should check the path relative to root search paths
        """
        # Given
        mock_os = MagicMock()
        mock_get_os.return_value = mock_os
        mock_os.root_search_paths = [Path('/mock/root1'), Path('/mock/root2')]
        self.resolver.drive_path = None

        path = 'relative/path/to/file.txt'
        expected_path = '/relative/path/to/file.txt'

        # When
        with patch.object(Path, 'is_absolute', return_value=False):
            with patch.object(Path, 'exists', side_effect=[True, False]):
                result = self.resolver.resolve(path)

        # Then
        assert result == expected_path

    @patch('gdriveresolver.resolver.locate_google_drive')
    @patch('gdriveresolver.resolver.get_operating_system')
    def test_file_not_found_must_resolve(self, mock_get_os, mock_locate_drive):
        """
        Given a non-existent file
        When must_resolve is True
        Then it should raise a FileNotFoundError
        """
        # Given
        mock_os = MagicMock()
        mock_get_os.return_value = mock_os
        mock_os.root_search_paths = [Path('/mock/root1'), Path('/mock/root2')]
        mock_locate_drive.return_value = None

        path = 'nonexistent/file.txt'

        # When
        with patch.object(Path, 'is_absolute', return_value=False):
            with patch.object(Path, 'exists', return_value=False):
                with self.assertRaises(FileNotFoundError):
                    self.resolver.resolve(path, must_resolve=True)

    @patch('gdriveresolver.resolver.locate_google_drive')
    @patch('gdriveresolver.resolver.get_operating_system')
    def test_file_not_found_no_must_resolve(self, mock_get_os, mock_locate_drive):
        """
        Given a non-existent file
        When must_resolve is False
        Then it should return None
        """
        # Given
        mock_os = MagicMock()
        mock_get_os.return_value = mock_os
        mock_os.root_search_paths = [Path('/mock/root1'), Path('/mock/root2')]
        mock_locate_drive.return_value = None

        path = 'nonexistent/file.txt'

        # When
        with patch.object(Path, 'is_absolute', return_value=False):
            with patch.object(Path, 'exists', return_value=False):
                result = self.resolver.resolve(path, must_resolve=False)

        # Then
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
