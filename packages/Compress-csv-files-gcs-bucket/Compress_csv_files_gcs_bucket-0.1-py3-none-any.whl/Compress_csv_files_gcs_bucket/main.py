import io
import zipfile
from google.cloud import storage


def compress_csv_files_gcs_bucket(bucket_name, prefix, output_zip_name, output_zip_prefix=None):
    # Create a client to interact with Google Cloud Storage
    client = storage.Client()

    # Get the bucket containing the files
    bucket = client.get_bucket(bucket_name)

    # Create an in-memory buffer to store the zip file
    zip_buffer = io.BytesIO()

    # Create a ZipFile object
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        # Iterate over each file in the bucket
        blobs = bucket.list_blobs(prefix=prefix)
        for blob in blobs:

            if 'csv' in blob.name:
                # Read the file content
                file_content = blob.download_as_string()
                # Add the file to the zip archive with its name, optionally removing the prefix
                zip_filename = blob.name[len(prefix):] if prefix and blob.name.startswith(prefix) else blob.name
                zip_file.writestr(zip_filename, file_content)

    # Write the zip file content to the GCS bucket
    zip_buffer.seek(0)
    output_blob_name = f"{output_zip_prefix}/{output_zip_name}" if output_zip_prefix else output_zip_name
    output_blob = bucket.blob(output_blob_name)
    output_blob.upload_from_file(zip_buffer, content_type='application/zip')

    print(f"All files with prefix '{prefix}' in bucket '{bucket_name}' zipped into '{output_blob_name}' and saved back to the same bucket.")
