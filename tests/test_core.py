import os
import tempfile
import zipfile
from unittest import TestCase, mock

from flask import Flask

from head_switcher.core import load_from_package_resources, load_from_file_path
from head_switcher.install import install_to_flask


class TestLoader(TestCase):

    @mock.patch('importlib.resources.path')
    def test_load_frontend_assets_from_pkg(self, MockPkgPath):
        with tempfile.TemporaryDirectory() as t:
            fake_path = os.path.join(t, 'fake.zip')
            with zipfile.ZipFile(fake_path, 'w') as zip_ref:
                zip_ref.writestr('build/file1.txt', 'content1')
                zip_ref.writestr('build/file2.txt', 'content2')
                zip_ref.writestr('build/dir/', '')

            class FakePkgCtx:
                def __enter__(self):
                    return fake_path

                def __exit__(self, exc_type, exc_val, exc_tb):
                    pass

            MockPkgPath.return_value = FakePkgCtx()

            result = load_from_package_resources('my_module', 'my-frontend.frontend')

            self.assertEqual(
                result,
                {
                    'file1.txt': b'content1',
                    'file2.txt': b'content2'
                }
            )

            self.assertEqual(('my_module', 'my-frontend.frontend'), MockPkgPath.call_args.args)

    def test_load_frontend_assets_from_path(self):
        with tempfile.TemporaryDirectory() as t:
            fake_path = os.path.join(t, 'fake.zip')
            with zipfile.ZipFile(fake_path, 'w') as zip_ref:
                zip_ref.writestr('build/file1.txt', 'content1')
                zip_ref.writestr('build/file2.txt', 'content2')
                zip_ref.writestr('build/dir/', '')

            result = load_from_file_path(fake_path)

            self.assertEqual(
                result,
                {
                    'file1.txt': b'content1',
                    'file2.txt': b'content2'
                }
            )

    def test_empty_frontend(self):
        app = Flask(__name__, static_folder=None)
        frontend_assets = {
            'some-wired-file': '?'
        }
        with self.assertWarns(UserWarning):
            install_to_flask(frontend_assets, app)
        testing_client = app.test_client()

        with testing_client.get('/') as resp:
            self.assertEqual(404, resp.status_code)
            self.assertEqual('', resp.text)

        with testing_client.get('/some-missing-file') as resp:
            self.assertEqual(404, resp.status_code)
            self.assertEqual('', resp.text)

        with testing_client.get('/some-wired-file') as resp:
            self.assertEqual(200, resp.status_code)
            self.assertEqual('?', resp.text)
            self.assertEqual('application/octet-stream', resp.mimetype)

    def test_normal_frontend(self):
        app = Flask(__name__, static_folder=None)
        frontend_assets = {
            'index.html': 'main ui',
            'some-wired-file': '?'
        }
        install_to_flask(frontend_assets, app)
        testing_client = app.test_client()

        with testing_client.get('/') as resp:
            self.assertEqual(200, resp.status_code)
            self.assertEqual('main ui', resp.text)

        with testing_client.get('/some-missing-file') as resp:
            self.assertEqual(200, resp.status_code)
            self.assertEqual('main ui', resp.text)

        with testing_client.get('/some-wired-file') as resp:
            self.assertEqual(200, resp.status_code)
            self.assertEqual('?', resp.text)
            self.assertEqual('application/octet-stream', resp.mimetype)
