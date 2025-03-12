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
    
    


def delete_playlist_data(directory_path):
    """
    Deletes all files within the specified directory.

    Args:
        directory_path (str): The path to the directory.
    """
    try:
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)

            # Check if it's a file (not a subdirectory)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            elif os.path.isdir(file_path):
                print(f"Skipping directory: {file_path}") #Optionally handle subdirectories here.
            else:
                 print(f"Skipping unknown item: {file_path}")

        print(f"Finished deleting files in: {directory_path}")

    except FileNotFoundError:
        print(f"Error: Directory not found: {directory_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
