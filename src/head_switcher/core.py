import importlib.resources
import zipfile
import os


def load_from_package_resources(package_name, asset_name, prefix='build/'):
    with importlib.resources.path(package_name, asset_name) as asset_zip_path:
        return load_from_file_path(asset_zip_path, prefix)


def load_from_file_path(filepath, prefix='build/'):
    frontend_assets = {}
    if os.path.exists(filepath):
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                if file_info.is_dir():
                    continue
                if file_info.filename.startswith(prefix):
                    with zip_ref.open(file_info) as file:
                        file_content = file.read()
                        frontend_assets[file_info.filename[len(prefix):]] = file_content
    return frontend_assets


def build_pack(folder_to_zip, output_zip_filename):
    if not os.path.exists(folder_to_zip):
        raise FileNotFoundError()
    with zipfile.ZipFile(output_zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_to_zip):
            for file in files:
                file_path = os.path.join(root, file)
                new_file_path = "build/" + os.path.relpath(file_path, folder_to_zip)
                zipf.write(file_path, arcname=new_file_path)
