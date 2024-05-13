from google.cloud import storage
import chardet
import io
import pandas as pd


def consolidate_csv_from_gcs(bucket_name, prefix, merged_file_name, output_bucket_name, output_bucket_name_prefix = None):

    # If output_bucket_name_prefix is not provided, use an empty string
    if output_bucket_name_prefix is None:
        output_bucket_name_prefix = prefix

    # Create a client to interact with Google Cloud Storage
    client = storage.Client()

    # Get the bucket containing the CSV files
    bucket = client.get_bucket(bucket_name)

    # List all the files with the given prefix
    blobs = bucket.list_blobs(prefix=prefix)

    # Create an empty list to store DataFrames
    dfs = []

    # Iterate over each CSV file in the bucket
    for blob in blobs:

        if '.csv' in blob.name:
            
            # Read CSV from GCS into a DataFrame
            print("Reading File -> ", blob.name)

            with blob.open("rb") as f:
                raw_data = f.read()
                # Detecting the encoding of the file being accessed.
                encoding = chardet.detect(raw_data)['encoding']
                csv_content = io.BytesIO(raw_data)
                print("Encoding detected ->", encoding)

            df = pd.read_csv(csv_content, encoding=encoding)

            # Append the DataFrame to the list
            print("Appending File- ", blob.name)
            dfs.append(df)

        else:
            continue

    # Concatenate all DataFrames in the list vertically
    merged_df = pd.concat(dfs, ignore_index=True)

    # Write the merged DataFrame to a BytesIO object
    merged_csv_bytesio = io.BytesIO()
    merged_df.to_csv(merged_csv_bytesio, index=False)
    merged_csv_bytesio.seek(0)

    # Create a client for the output bucket
    output_bucket = client.bucket(output_bucket_name)

    # Upload the merged CSV file to the output bucket
    merged_file_name = f"{output_bucket_name_prefix}/{merged_file_name}"
    print("Merged file name and location -> ", merged_file_name)
    output_blob = output_bucket.blob(merged_file_name)
    output_blob.upload_from_file(merged_csv_bytesio, content_type='text/csv')

    print(f"Merged CSV file saved as {merged_file_name}")
