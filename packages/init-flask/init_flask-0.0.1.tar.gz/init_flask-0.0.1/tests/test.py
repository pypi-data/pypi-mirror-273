import unittest
from unittest.mock import patch
import os
from src.init_flask import init

class TestInitFunction(unittest.TestCase):
    def setUp(self):
        self.test_project_name = "test_project"
        self.test_path = os.path.join(os.getcwd(), "test_dir")
        os.makedirs(self.test_path)

    def tearDown(self):
        os.rmdir(self.test_path)

    @patch("my_project.echo_message")
    def test_init_success(self, mock_echo_message):
        init(showpg=True, libs="", hardcore=False, path=self.test_path, project_name=self.test_project_name)
        
        # Asserting that the appropriate echo messages were called with the correct arguments
        expected_calls = [
            ((f"Initializing......", True), {}),
            ((f"Creating folder......", True), {}),
            ((f"Folder created successfully", True, 'success'), {}),
            ((f"Creating virtual environment......", True), {}),
            ((f"venv created successfully", True, 'success'), {}),
            ((f"Creating files......", True), {}),
            ((f"Successfully initialized Flask environment🎉", True, 'success'), {})
        ]
        self.assertEqual(mock_echo_message.call_args_list, [unittest.mock.call(*args, **kwargs) for args, kwargs in expected_calls])

if __name__ == "__main__":
    unittest.main()
