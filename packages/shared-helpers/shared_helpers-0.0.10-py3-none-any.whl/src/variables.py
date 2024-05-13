import os
#from dotenv import load_dotenv
#load_dotenv()

# default service_account_user
SA01_IAM_TOKEN = os.environ.get('SA01_IAM_TOKEN')
SA01_IAM_TOKEN_EXPIRY = os.environ.get('SA01_IAM_TOKEN_EXPIRY')
SA01_JSON_FILE_PATH = os.environ.get('SA01_JSON_FILE_PATH')
SA01_API_KEY = os.environ.get('SA01_API_KEY')
SA01_CF_ENDPOINT_URL = os.environ.get('SA01_CF_ENDPOINT_URL')

# sbbid
SBBID_X_API_KEY = os.environ.get('SBBID_X_API_KEY')
SBBID_ENVIRONMENT = os.environ.get('SBBID_ENVIRONMENT')