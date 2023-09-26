import tempfile
from unittest import TestCase
import os
import zipfile

from head_switcher.cli import cli
from head_switcher.core import build_pack


class TestPacker(TestCase):
    def setUp(self):
        # Create a temporary directory with some test files for testing
        self.t = tempfile.TemporaryDirectory()
        self.temp_dir = os.path.join(self.t.name, 'f')
        self.temp_dir_output_file = os.path.join(self.temp_dir, 'out-test.frontend')

        os.makedirs(self.temp_dir, exist_ok=True)

        with open(os.path.join(self.temp_dir, "index.html"), "w") as f:
            f.write("This is index.html")
        with open(os.path.join(self.temp_dir, "styles.css"), "w") as f:
            f.write("This is styles.css")

        self.cwd = os.getcwd()
        os.chdir(self.t.name)

    def tearDown(self):
        self.t.cleanup()
        os.chdir(self.cwd)

    def test_build_pack(self):
        # Define the test input and expected output
        input_folder = self.temp_dir

        # Call the function being tested
        build_pack(input_folder, self.temp_dir_output_file)

        # Assert that the zip file was created
        self.assertTrue(os.path.exists(self.temp_dir_output_file))

        # Verify the content of the zip file
        with zipfile.ZipFile(self.temp_dir_output_file, "r") as zipf:
            # List the files in the zip archive
            file_list = zipf.namelist()

            # Check if the files in the zip archive have the "build/" prefix
            for file_name in file_list:
                self.assertTrue(file_name.startswith("build/"))

    def test_build_pack_nonexistent_folder(self):
        # Test the function with a non-existent folder
        input_folder = os.path.join(self.t.name, "nonexistent_folder")
        output_zip_filename = self.temp_dir_output_file

        # Call the function and expect it to raise an exception
        with self.assertRaises(FileNotFoundError):
            build_pack(input_folder, output_zip_filename)

    def test_cli_non_exist(self):
        input_folder = os.path.join(self.t.name, "nonexistent_folder")

        with self.assertRaises(FileNotFoundError):
            cli([input_folder, '-o', self.temp_dir_output_file])

    def test_cli_default_out(self):
        cli([self.temp_dir])
        with zipfile.ZipFile(
                os.path.join(self.t.name, 'out.frontend')
                , "r") as zipf:
            # List the files in the zip archive
            file_list = zipf.namelist()

            # Check if the files in the zip archive have the "build/" prefix
            for file_name in file_list:
                self.assertTrue(file_name.startswith("build/"))

    def test_cli(self):
        output_zip_filename = self.temp_dir_output_file
        cli([self.temp_dir, '-o', output_zip_filename])
        with zipfile.ZipFile(output_zip_filename, "r") as zipf:
            # List the files in the zip archive
            file_list = zipf.namelist()

            # Check if the files in the zip archive have the "build/" prefix
            for file_name in file_list:
                self.assertTrue(file_name.startswith("build/"))
