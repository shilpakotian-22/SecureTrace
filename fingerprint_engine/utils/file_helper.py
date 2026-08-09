import os
import shutil


def copy_document(source_path, recipient):

    filename = os.path.basename(source_path)

    name, extension = os.path.splitext(filename)

    safe_recipient = recipient.replace(" ", "_")

    new_filename = f"{name}_{safe_recipient}{extension}"

    destination_folder = os.path.join(
        "generated_documents",
        "fingerprinted"
    )

    os.makedirs(
        destination_folder,
        exist_ok=True
    )

    destination_path = os.path.join(
        destination_folder,
        new_filename
    )

    shutil.copy2(
        source_path,
        destination_path
    )

    return destination_path