import json
import requests

from urllib3.util import Retry
from requests.adapters import HTTPAdapter
from yandex_tracker_client import TrackerClient

req = requests.Session()
retries = Retry(total=5,
                backoff_factor=2,
                status_forcelist=[429, 500, 502, 503, 504])

req.mount('http://', HTTPAdapter(max_retries=retries))

class TrackerHelper:
    def __init__(self, iam_token, cloud_org_id='bpf6lemclm2bnd2i9cce', x_org_id='6615873'):
        self.iam_token = iam_token
        self.cloud_org_id = cloud_org_id
        self.headers_dict = {'Authorization': f'Bearer {iam_token}', 'X-Org-ID': x_org_id}
        self.default_client = TrackerClient(iam_token=self.iam_token, cloud_org_id=self.cloud_org_id)


    def issues_import_issue(self, issue_dict):
        payload = json.dumps(issue_dict)
        response = req.post(f'{TRACKER_URL}/v2/issues/_import', headers=self.headers_dict, data=payload)
        return response.json()

    def issues_comments_import_comment(self, issue_key,comment_dict):
        payload = json.dumps(comment_dict)
        response = req.post(f'{TRACKER_URL}/v2/issues/{issue_key}/comments/_import', headers=self.headers_dict, data=payload)
        return response.json()


    def issues_get_issue(self, issue_key):
        response = req.get(f'{TRACKER_URL}/v2/issues/{issue_key}', headers=self.headers_dict)
        return response.json()
    
    def issues_issue_update(self, issue_key,issue_field,value):
        payload = json.dumps({issue_field: value})
        response = req.patch(f"{TRACKER_URL}/v2/issues/{issue_key}", headers=self.headers_dict, data=payload)
        return response.json()

    def comments_get_comments(self, issue_key=None):
        response = req.get(f'{TRACKER_URL}/v2/issues/{issue_key}/comments', headers=self.headers_dict)
        return response.json()

    def issues_comments_get_comment(self, issue_key,comment_id):
        response = req.get(f'{TRACKER_URL}/v2/issues/{issue_key}/comments/{comment_id}', headers=self.headers_dict)
        return response.json()

    def issues_comments_delete_comment(self, issue_key,comment_id):
        response = req.delete(f'{TRACKER_URL}/v2/issues/{issue_key}/comments/{comment_id}', headers=self.headers_dict)
        return response.json()


    def checklists_create_checklist(self, issue_key,checklist_dict):
        payload = json.dumps(checklist_dict)
        response = req.post(f'{TRACKER_URL}/v2/issues/{issue_key}/checklistItems', headers=self.headers_dict,data=payload)
        return response.json()


    def users_get_user_uid_by_login(self, username):
        response = req.get(f'{TRACKER_URL}/v2/users/login:{username}', headers=self.headers_dict)
        return response.json()
    '''
    def users_get_user_info_by_cloud_uid(self, cloud_uid):
        cloud_user = cloud.cloud_get_user_info(cloud_uid)
        print(cloud_user)
        user_ldap = cloud_user.get('samlUserAccount').get('nameId')
        response = req.get(f'{TRACKER_URL}/v2/users/login:{user_ldap}', headers=self.headers_dict)
        return response.json()
    '''
    def users_get_user_info(self, user_uid):
        payload = {}
        response = req.get(f'{TRACKER_URL}/v2/users/{user_uid}', headers=self.headers_dict, params=payload)
        return response.json()

    def users_get_service_account_by_displayname(self, service_account_displayname):
        users = self.default_client.users.get_all()
        user_dict = {}
        for user in users:
            if user.display == service_account_displayname:
                user_dict['uid'] = user.uid
                user_dict['login'] = user.login
                user_dict['display'] = user.display
        return user_dict

    def users_is_user_have_queue_permission(self, queue_key, user_id, permission_for_search):
        queue = self.default_client.queues[queue_key]
        queue_permissions = {'grant': queue.permissions.grant.users, 'write': queue.permissions.write.users, 'create': queue.permissions.create.users, 'read': queue.permissions.read.users}
        permission = queue_permissions[permission_for_search]
        result = next((obj for obj in permission if obj.id == user_id),False)
        if result:
            return True
        else:
            return False

    def users_is_user_group_member(self, login='',tracker_group_id=''):
        group_members = self.tracker_get_group_members_by_group_id(tracker_group_id)
        result = next((obj for obj in group_members if obj.get('login') == login),False)
        return result

    def users_get_user_last_login_date(self, user_uid):
        response = req.get(f'{TRACKER_URL}/v2/users/{user_uid}', headers=self.headers_dict)
        return response.json().get('lastLoginDate')


    def fields_get_field_version(self, field):
        payload = {}
        response = req.get(f'{TRACKER_URL}/v2/fields/{field}', headers=self.headers_dict, data=payload)
        return(response.json()['version'])

    def fields_get_field_values(self, field):
        payload = {}
        response = req.get(f'{TRACKER_URL}/v2/fields/{field}', headers=self.headers_dict, data=payload)
        if (field == 'domains'):
            return(response.json()['optionsProvider']['values'])
        else:
            return(response.json())

    def fields_field_update_values(self, field,values):
        payload = {
            "optionsProvider":
                {
                    "type": "FixedListOptionsProvider",
                    "values": values
                }
        }
        current_field_version = self.tracker_get_field_version(field)
        response = req.patch(f'{TRACKER_URL}/v2/fields/{field}?version={str(current_field_version)}', headers=self.headers_dict, data=json.dumps(payload))
        return(response.json())
        
    def queues_update_permission(self, queue,permission,group_or_user,action,member):
        member = [member]
        payload = {
            permission:{
                group_or_user:{
                    action: member
                }
            }
        }
        response = req.patch(f'{TRACKER_URL}/v2/queues/{str(queue)}/permissions', headers=self.headers_dict, data=json.dumps(payload))
        return(response)

    def queues_get_queues(self):
        payload = {}
        result = {}
        response = req.get(f'{TRACKER_URL}/v2/queues?perPage=10000', headers=self.headers_dict, data=payload)
        for i in response.json():
            #print(i)
            if (response.status_code ==200):
                result.update({i['id']: i['key']})
        return(result)

    def queues_get_queue_info(self, queue):
        payload = {'expand':'all'}
        result = {}
        response = req.get(f'{TRACKER_URL}/v2/queues/{queue}', headers=self.headers_dict, data=payload)
        return response.json()
    
    def queues_list_queue_permissions(self, queue_key, permission_for_search):
        group_list = []
        queue = self.default_client.queues[queue_key]
        queue_permissions = {'grant': queue.permissions.grant.groups, 'write': queue.permissions.write.groups, 'create': queue.permissions.create.groups, 'read': queue.permissions.read.groups}
        permission = queue_permissions[permission_for_search]
        for p in permission:
            group_list.append(p.id)
        return group_list

    def queues_queue_get_components(self, queue_key=None):
        payload = {'queue':queue_key}
        response = req.get(f'{TRACKER_URL}/v2/components', headers=self.headers_dict, data=payload)
        return response.json()

    def queues_queue_create_component(self, queue_key=None,component_name=None,description='',lead=None,assignAuto=False):
        component_dict = {'queue':queue_key, 'name':component_name,'description': description,'lead': lead,'assignAuto': assignAuto}
        payload = json.dumps(component_dict)
        print(payload)
        response = req.post(f'{TRACKER_URL}/v2/components', headers=self.headers_dict, data=payload)
        return response.json()

    

    def groups_is_group_have_queue_permission(self, queue_key, group_id, permission_for_search):
        queue = self.default_client.queues[queue_key]
        queue_permissions = {'grant': queue.permissions.grant.groups, 'write': queue.permissions.write.groups, 'create': queue.permissions.create.groups, 'read': queue.permissions.read.groups}
        permission = queue_permissions[permission_for_search]
        result = next((obj for obj in permission if obj.id == group_id),False)
        if result:
            return True
        else:
            return False
    '''
    def groups_get_group_members_by_group_id(self, tracker_group_id=''):
        response = req.get(f'{TRACKER_URL}/v2/groups/'+str(tracker_group_id), headers=self.headers_dict)
        tracker_group_description = response.json().get('name')
        cloud_group_id = cloud.cloud_get_group_by_description(tracker_group_description).get('id')
        group_members = cloud.cloud_get_group_members(cloud_group_id)
        return group_members
    '''




TRACKER_URL = 'https://api.tracker.yandex.net'