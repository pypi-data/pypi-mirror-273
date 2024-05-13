import json
import requests

from urllib3.util import Retry
from requests.adapters import HTTPAdapter

req = requests.Session()
retries = Retry(total=5,
                backoff_factor=2,
                status_forcelist=[429, 500, 502, 503, 504])

req.mount('http://', HTTPAdapter(max_retries=retries))

class CloudHelper:
    def __init__(self, iam, organizationId='bpf6lemclm2bnd2i9cce', federationId='bpfibfn71tu9suogt3jg'):
        self.iam = iam
        self.organizationId = organizationId
        self.federationId = federationId 
        self.headers_dict = {'Authorization': f'Bearer {iam}', 'organizationId':organizationId}

    def cloud_get_all_groups(self):
        params_dict = {'organizationId':self.organizationId,'pageSize':'1000'}
        response = req.get('https://organization-manager.api.cloud.yandex.net/organization-manager/v1/groups', headers=self.headers_dict, params=params_dict)
        return(response.json().get('groups'))

    def cloud_get_group(self,group_id):
        response = req.get(f'https://organization-manager.api.cloud.yandex.net/organization-manager/v1/groups/{group_id}', headers=self.headers_dict)
        return(response.json())

    def cloud_add_user_to_group(self, user_id, group_id):
        data_dict = json.dumps({"memberDeltas": [{
        "action": "ADD",
        "subjectId": f"{user_id}"}]})
        response = req.post(f'https://organization-manager.api.cloud.yandex.net/organization-manager/v1/groups/{group_id}:updateMembers', headers=self.headers_dict, data=data_dict)
        return(response.json())

    def cloud_remove_user_from_group(self, user_id, group_id):
        data_dict = json.dumps({"memberDeltas": [{
        "action": "REMOVE",
        "subjectId": f"{user_id}"}]})
        response = req.post(f'https://organization-manager.api.cloud.yandex.net/organization-manager/v1/groups/{group_id}:updateMembers', headers=self.headers_dict, data=data_dict)
        return(response.json())

    def cloud_get_group_by_description(self, group_description):
        all_groups = self.cloud_get_all_groups()
        for group in all_groups:
            if group.get('description') == group_description:
                return group

    def cloud_get_group_by_name(self, group_name):
        all_groups = self.cloud_get_all_groups()
        for group in all_groups:
            if group.get('name') == group_name:
                return group

    def cloud_get_user_info(self, userAccountId,federationId):
        response = req.get(f'https://iam.api.cloud.yandex.net/iam/v1/userAccounts/{userAccountId}', headers=self.headers_dict)
        return response.json()

    def cloud_get_user_account_by_id(self, userAccountId,federationId):
        user_dict = {}
        response = req.get(f'https://iam.api.cloud.yandex.net/iam/v1/userAccounts/{userAccountId}', headers=self.headers_dict)
        if(response.json().get('samlUserAccount').get('federationId') == federationId):
            try:
                user_dict['cloud_id'] = response.json().get('id')
                user_dict['login'] = response.json().get('samlUserAccount').get('nameId')
                user_dict['email'] = response.json().get('samlUserAccount').get('attributes').get('email').get('value')[0]
                user_dict['firstName'] = response.json().get('samlUserAccount').get('attributes').get('firstName').get('value')[0]
                user_dict['lastName'] = response.json().get('samlUserAccount').get('attributes').get('lastName').get('value')[0]
                user_dict['federationId'] = response.json().get('samlUserAccount').get('federationId')
            except Exception as e:
                print(str(e))
        return(user_dict)
        

    def cloud_get_group_members(self, group_id):
        user_dict = []
        url = f'https://organization-manager.api.cloud.yandex.net/organization-manager/v1/groups/{group_id}:listMembers'
        response = req.get(url, headers=self.headers_dict)
        users = response.json().get('members')
        if (len(users)):
            for user in users:
                user = self.cloud_get_user_account_by_id(user.get('subjectId'))
                if (len(user)):
                    user_dict.append(user)
            return(user_dict)
        
    def cloud_list_group_members(self, group_id):
        user_dict = []
        url = f'https://organization-manager.api.cloud.yandex.net/organization-manager/v1/groups/{group_id}:listMembers'
        response = req.get(url, headers=self.headers_dict)
        users = response.json().get('members')
        for user in users:
            user_dict.append(user.get('subjectId'))
        return(user_dict)


