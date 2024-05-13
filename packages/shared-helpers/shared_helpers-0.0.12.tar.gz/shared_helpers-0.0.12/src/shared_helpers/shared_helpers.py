import os
import time
#from variables import *
from shared_helpers.yandex.organization.organization_helper import CloudHelper
from shared_helpers.yandex.tracker.tracker_helper import TrackerHelper
from shared_helpers.lm.sbbid.sbbid_helper import SbbIdHelper
from shared_helpers.functions import TokenHelper

#iam_token_from_file = token_helper.get_iam_token_from_file()

def get_iam_token():
    iam_token = {}
    if 'SA01_IAM_TOKEN' in os.environ and 'SA01_IAM_TOKEN_EXPIRY' in os.environ and int(os.environ.get('SA01_IAM_TOKEN_EXPIRY')) - int(time.time()) > 1200:
        #print('from env')
        iam_token['SA01_IAM_TOKEN'] = os.environ.get('SA01_IAM_TOKEN')
        iam_token['SA01_IAM_TOKEN_EXPIRY'] = os.environ.get('SA01_IAM_TOKEN_EXPIRY')
    elif 'SA01_JSON_FILE_PATH' in os.environ and os.environ.get('SA01_JSON_FILE_PATH') is not None:
        #print('from file')
        iam_token['SA01_IAM_TOKEN'] = TokenHelper(json_file_path=os.environ.get('SA01_JSON_FILE_PATH')).get_iam_token_from_file()
        iam_token['SA01_IAM_TOKEN_EXPIRY'] = TokenHelper(json_file_path=os.environ.get('SA01_JSON_FILE_PATH')).get_iam_token_from_file()
    elif 'SA01_API_KEY' in os.environ and 'SA01_CF_ENDPOINT_URL' in os.environ:
        #print('from endpoint')
        token_helper = TokenHelper(api_key=os.environ.get('SA01_API_KEY'), endpoint_url=os.environ.get('SA01_CF_ENDPOINT_URL')).get_iam_token_from_endpoint()
        iam_token['SA01_IAM_TOKEN'] = token_helper.get('token').get('access_token')
        iam_token['SA01_IAM_TOKEN_EXPIRY'] = str(int(time.time()) + int(token_helper.get('token').get('expires_in')))
    return iam_token
            
def save_iam_token_to_environment(iam_token):
    #print('old:',os.environ.get('SA01_IAM_TOKEN'))
    os.environ["SA01_IAM_TOKEN"] = iam_token.get('SA01_IAM_TOKEN')
    os.environ["SA01_IAM_TOKEN_EXPIRY"] = iam_token.get('SA01_IAM_TOKEN_EXPIRY')
    #print('new:',os.environ.get('SA01_IAM_TOKEN'))

iam_token = get_iam_token()

save_iam_token_to_environment(iam_token)

#sbbid_client = SbbIdHelper()
#cloud_client = CloudHelper(iam_token)
#tracker_client = TrackerHelper(iam_token)
#print(cloud_client.cloud_get_all_groups())
#print(tracker_client.queues_get_queues())
#print(sbbid_client.get_domains())
