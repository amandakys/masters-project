import os
from azure.storage.blob import BlobServiceClient


def createBlobConnectionClient(): 
    connect_str = "DefaultEndpointsProtocol=https;AccountName=mastersproject;AccountKey=VgzJTcn2ZqBXV/hXIAiBdi43oFf+9pcaqx67hhbnwAYPia9N5BzpuksvdWVqmG5U9ASY0Fh/wzez+AStGrAjog==;EndpointSuffix=core.windows.net"
    
    #  connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    return blob_service_client

def upload_file_to_azure(blob_name):
      # azure stuff starts here 
    blob_service_client = createBlobConnectionClient()

    # upload_file_path = os.path.join("./media/"+username + "/experimentone", file_name)
    # upload_file_path = "./media/" + username + "/experimentone/" + file_name
    upload_file_path = "./media/" + blob_name

    print("\nChecking blob does not already exist ...")
    #check blob does not already exist 
    # blob_name = username + '/experimentone/'+ file_name

    container_client = blob_service_client.get_container_client("media")
    
    hasBlob = False

    blob_list = container_client.list_blobs()

    for blob in blob_list: 
        if blob.name == blob_name :
            hasBlob = True
            print (blob_name + ' already exists')

    if not hasBlob:
        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container='media', blob=blob_name)

        print("\nUploading to Azure Storage as blob:\n\t" + blob_name)

        # Upload the created file
        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data)

def azure_has_blob(blob_name):
    blob_service_client = createBlobConnectionClient()
    container_client = blob_service_client.get_container_client("media")
    blob_list = container_client.list_blobs()

    # blob_name = username + '/experimentone/'+ file_name

    hasBlob = False
    
    for blob in blob_list: 
        if blob.name == blob_name :
            hasBlob = True
            print (file_name + ' already exists')
    
    return hasBlob

def delete_file(blob_name):
    blob_service_client = createBlobConnectionClient()
    container_client = blob_service_client.get_container_client("media")
    container_client.delete_blob(blob=blob_name)


