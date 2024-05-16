import pathlib as paths
import zipfile

from maat_machine.pprint import displayitwell
import maat_machine.filesystem as mt_fs

def unzip_to_directory(zip_file: paths.Path, destination_directory: paths.Path):
    assert zip_file.is_file()
    assert mt_fs.directory_exists(destination_directory)
    with zipfile.ZipFile(str(zip_file), 'r') as zip_reference:
        zip_reference.extractall(destination_directory)
        extracted_files = zip_reference.namelist()
        displayitwell(f"ZIP file \"{zip_file}\" is extracted to \"{destination_directory}\"; Extracted files count: {len(extracted_files)}", font_style='oblique', font_weight='bold')
