import zipfile
import os

async def zip_folder(folder_path, zip_filename):
    """Zip all files inside the folder."""
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)  # Keep folder structure
                zipf.write(file_path, arcname)
    return zip_filename