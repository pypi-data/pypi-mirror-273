from google.cloud import storage
from google.cloud import bigquery
import os
import json
import pandas as pd
from datetime import datetime as dt


def process_json_file_streaming(dataset_id, table_name, project_id, bucket_name, 
                      source_folder_name, destination_folder_name, 
                      chunk_size = 10000, add_record_entry_time = False, 
                      add_file_name = False):

    ## Define GCS storage and Bigquery storage clients
    storage_client = storage.Client()
    client = bigquery.Client()

    ## Obtain the GCS bucket object
    bucket = storage_client.get_bucket(bucket_name)

    ##Create the folder name
    prefix = source_folder_name + '/'

    ## List the files contained in the folder(inside the GCS bucket) which contains the file to be processed
    blobs = bucket.list_blobs(prefix=prefix, delimiter='/')

    ## Iterate through all the files contained in the folder
    for blob in blobs:

        ## Print the filename
        print(blob)

        ## Check if its a json file
        if '.json' not in blob.name:
            print("Not a json file - ", blob)
            continue
        
        ## Obtain the complete path of the json file being currently processed.
        final_blob = blob
        filepath = bucket_name + '/' + blob.name
        filename = os.path.basename(filepath)
        # json_file_path = 'gs://' + filepath

        print("Processing - ", filepath)
        print(final_blob)

        ## Read the json file 
        data = final_blob.open("r", encoding='utf-8')
        print("Data load has completed.")

        ## Iterating through each line in the data file and converting a valid JSON string into a Python data structure(like dict or list)
        json_data = [json.loads(line)
                        for line in data]

        
        ## Obtain current timestamp. 
        currenttime=dt.now()

        # copy to new destination
        bucket.copy_blob(final_blob, bucket, str(final_blob.name).replace(source_folder_name, destination_folder_name))
        
        print(f'File moved from ', final_blob.name, 'to ', str(final_blob.name).replace(source_folder_name, destination_folder_name))

        # delete in old destination
        final_blob.delete()

        ## Obtain the dataframe from the json data that was read
        json_data = pd.DataFrame.from_dict(json_data)        
        
        # Convert entire DataFrame to string
        json_data=json_data.applymap(str)
        print(json_data.dtypes)

        # Add additional columns if the user has requested.
        if add_record_entry_time:
            json_data['record_entry_time'] = currenttime

        if add_file_name:
            json_data['file_name'] = filename

        print("DataFrame has been created")

        ## Remove special characters from file name 
        json_data.columns =  json_data.columns.str.strip().str.replace(" ","").str.replace("/","").str.replace("-","")

        ## Description of the dataframe
        df= json_data
        print("Description of the dataframe")
        print(df.describe())
        
        # Extract chunk of records that need to be inserted in one iteration
        chunks = [df[i:i+chunk_size] for i in range(0, len(df), chunk_size)]
        
        ## Setup loading job for Bigquery
        job_config = bigquery.LoadJobConfig(autodetect=False, source_format=bigquery.SourceFormat.CSV, allow_jagged_rows = True, allow_quoted_newlines = True)
        
        ## Creating exact table name 
        table_id = project_id + "." + dataset_id + '.' + table_name

        ## Iterate through the chunks of records collected to be inserted.
        for idx, chunk in enumerate(chunks):
            print("---------------------------------------------------------------------")

            ## Description of each chunk
            print("Description of chunk of records being inserted")
            print(chunk.describe())
            print("About to push to Bigquery")

            ## Load table from dataframe.
            load_job = client.load_table_from_dataframe(chunk, table_id, job_config=job_config)  # Make an API request.
            load_job.result()
            
            ## Check how many records have been added until now.
            destination_table = client.get_table(table_id)  # Make an API request.
            print("Loaded {} rows.".format(destination_table.num_rows))

