from google.cloud import storage

def files_in_bucket(bucket_name, folder_name, filename_needed = True, file_object_needed = False, list_sub_folders = False):
  
  try:
    # Use the storage library to access the bucket.
    client = storage.Client()
    delimiter = '/'
    bucket = client.get_bucket(bucket_name)
    
    print("Bucket Name -> ", bucket_name)
    print("Folder Name -> ", folder_name)
    
    # Making the extraction robust
    if folder_name[-1] != '/':
      folder_name = folder_name + '/'
    if list_sub_folders == True:
      delimiter = None
    
    # Extract the contents of the location.
    sources = bucket.list_blobs(prefix=folder_name, delimiter = delimiter)

    # Creating empty lists to return the contents of the location.
    file_list = []
    file_list_names = []
    
    # Iterate over the contents of the bucket
    for blob in sources:
      print(blob)
      file_list_names.append(blob.name)
      file_list.append(bucket.blob(blob.name))

    # Check if the object of the files is needed.
    if file_object_needed == True and filename_needed == False:
      print("Returning a list of file objects")
      print("Returned value -> ", file_list)
      return file_list
    
    # Check if the filenames are needed.
    elif file_object_needed == False and filename_needed == True:
      print("Returning a list of file names")
      print("Returned value -> ", file_list_names)
      return file_list_names
    
    elif file_object_needed == True and filename_needed == True:
      print("Both Filenames and file object cannot be provided together. Please specify only one requirement")
    
  
  except Exception as e:
      # Code to handle other exceptions
      print("An error occurred:", e)
