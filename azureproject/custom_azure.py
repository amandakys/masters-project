from storages.backends.azure_storage import AzureStorage

class AzureStaticStorage(AzureStorage):
    account_name = 'mastersproject' # Must be replaced by your storage_account_name
    account_key = 'VgzJTcn2ZqBXV/hXIAiBdi43oFf+9pcaqx67hhbnwAYPia9N5BzpuksvdWVqmG5U9ASY0Fh/wzez+AStGrAjog==' # Must be replaced by your <storage_account_key>
    azure_container = 'static'
    expiration_secs = None

