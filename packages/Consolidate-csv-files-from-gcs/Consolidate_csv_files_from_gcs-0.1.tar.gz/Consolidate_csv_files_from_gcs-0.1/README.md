Python Library for Merging CSV Files from Google Cloud Storage

This library provides a function consolidate_csv_from_gcs that simplifies the process of merging multiple CSV files from a Google Cloud Storage (GCS) bucket into a single file.

**1. consolidate_csv_from_gcs(bucket_name, prefix, merged_file_name, output_bucket_name, output_bucket_name_prefix):**

The consolidate_csv_from_gcs function takes the following arguments:

*Parameters:*

1. bucket_name = "your-bucket-name"
2. prefix = "path/to/your/csv/files/"  # Include trailing slash
3. merged_file_name = "merged_data.csv"
4. output_bucket_name = "output-bucket-name"
5. output_bucket_name_prefix = "merged/data/"  # Optional, defaults to prefix


Return Value:

There is no return value as the result can be seen in the GCS bucket.

**Usage:**

```Python

from Consolidate_csv_files_from_gcs import consolidate_csv_from_gcs

consolidate_csv_from_gcs(
    bucket_name='source-bucket',
    prefix='data/',
    merged_file_name='consolidated.csv',
    output_bucket_name='destination-bucket',
    output_bucket_name_prefix='processed/'
)

```

*Explanation:*

The consolidate_csv_from_gcs function takes the following arguments:
1. bucket_name: (str) The name of the GCS bucket containing the CSV files.
2. prefix: (str) The prefix to filter files within the bucket (e.g., "path/to/your/csv/files/"). Include a trailing slash.
3. merged_file_name: (str) The desired name for the output merged CSV file.
4. output_bucket_name: (str) The name of the GCS bucket where the merged file will be saved.
5. output_bucket_name_prefix (str, optional): An optional prefix to add to the filename within the output bucket. Defaults to the prefix argument.

*Function Behaviour:*

1. Connects to GCS using storage.Client.
2. Retrieves the bucket specified by bucket_name.
3. Lists all files with the provided prefix and extension .csv.
4. Iterates through each CSV file: 
5. Reads the content with automatic encoding detection using chardet.
6. Creates a Pandas DataFrame from the CSV content.
7. Appends the DataFrame to a list.
8. Concatenates all DataFrames vertically into a single merged DataFrame.
9. Creates a BytesIO object to hold the merged CSV data in memory.
10. Writes the merged DataFrame to the BytesIO object using to_csv.
11. Connects to the output GCS bucket using storage.Client.
12. Creates a new blob object with the desired filename within the output bucket (including any output_bucket_name_prefix).
13. Uploads the merged CSV data (from BytesIO) to the output blob as a CSV file (content_type='text/csv').


**Additional Notes:**

1. This library uses the google-cloud-storage and pandas libraries. Ensure they are installed (pip install google-cloud-storage pandas).
2. The library automatically detects the encoding of the CSV files using chardet.
3. The merged file is written to a memory buffer (BytesIO) before uploading to GCS for efficiency.
 

I hope this README clarifies the usage of these functions for managing Alteryx workflows through Python. Feel free to ask if you have any further questions.
