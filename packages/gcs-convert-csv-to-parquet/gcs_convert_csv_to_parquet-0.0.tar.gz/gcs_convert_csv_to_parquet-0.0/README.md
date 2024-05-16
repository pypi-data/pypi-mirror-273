Python Library for Compressing Files in Google Cloud Storage

This Python library provides a function to convert a CSV file stored in a Google
Cloud Storage (GCS) bucket to a Parquet file and upload it back to the same
bucket.


*Functionality*
1. Downloads a CSV file from a specified GCS bucket.
2. Reads the CSV data into a pandas DataFrame.
3. Converts the DataFrame to an Arrow Table for efficient Parquet storage.
4. Uploads the Arrow Table as a Parquet file to the GCS bucket.
5. Optionally allows specifying an output folder within the bucket to store the
   Parquet file.

*Installation*
You'll need the following:
1. Python 3.6 or later
2. google-cloud-storage
3. pandas
4. pyarrow


Install them using pip:
```Bash
pip install google-cloud-storage pandas pyarrow
```

*Example Usage:*

```Python

from gcs_convert_csv_to_parquet import gcs_convert_csv_to_parquet

# Define your parameters
bucket_name = 'your-bucket-name'
csv_file = 'your-csv-file.csv'
parquet_file = 'your-output-file.parquet'
output_folder = 'optional-output-folder'  # Optional

# Convert CSV to Parquet and upload to GCS
gcs_convert_csv_to_parquet(bucket_name, csv_file, parquet_file, output_folder)

```


The gcs_convert_csv_to_parquet function takes the following arguments:

*Parameters:*

1. bucket_name (str): The name of the bucket containing the CSV file.
2. csv_file (str): The name of the CSV file to convert.
3. parquet_file (str): The desired name for the output Parquet file.
4. output_folder (str, optional): The folder within the bucket to store the Parquet file. If None, the file will be stored at the root level of the bucket.


*Notes*
1. This library assumes you have proper authentication set up to access Google
Cloud Storage.
2. The CSV file must be valid and well-formatted.
3. Error handling is included to catch potential exceptions during conversion or
upload.


*Example Usage*
This example converts a CSV file named data.csv to a Parquet file named
data.parquet and stores it in the output_folder within the specified bucket:


```Python
gcs_convert_csv_to_parquet("my-bucket", "data.csv", "data.parque
```

This will print a success message upon successful conversion and upload.