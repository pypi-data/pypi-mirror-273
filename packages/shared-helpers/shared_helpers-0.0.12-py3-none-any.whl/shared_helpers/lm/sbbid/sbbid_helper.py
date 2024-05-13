import requests
from urllib3.util import Retry
from requests.adapters import HTTPAdapter

req = requests.Session()
retries = Retry(total=5,
                backoff_factor=2,
                status_forcelist=[429, 500, 502, 503, 504])
req.mount('http://', HTTPAdapter(max_retries=retries))

class SbbIdHelper():
    def __init__(self, x_api_key=None, environment=None):
        self.x_api_key = x_api_key
        self.environment = environment
        self.headers_dict = {'x-api-key': x_api_key}
        if environment == 'external':
            self.BASE_URL = 'https://api.leroymerlin.ru:443/technologies/sbbid/catalogue/v1'
        else:
            self.BASE_URL = 'https://api.internal.leroymerlin.ru/technolosies/sbbid/infoproduct/v2'

    def get_domains(self):
        url = f'{self.BASE_URL}/domains'
        response = req.get(url, headers=self.headers_dict)
        return response.json()
    
    def get_domain_by_id(self, domainId):
        url = f'{self.BASE_URL}/domains/{domainId}'
        response = req.get(url, headers=self.headers_dict)
        return response.json()

    def get_domain_teams(self, domainId):
        url = f'{self.BASE_URL}/{domainId}/product-teams'
        response = req.get(url, headers=self.headers_dict)
        return response.json()

    def get_objects(self):
        url = f'{self.BASE_URL}/objects/'
        response = req.get(url, headers=self.headers_dict)
        return response.json()

    def get_object_by_id(self, objectId):
        url = f'{self.BASE_URL}/objects/{objectId}'
        response = req.get(url, headers=self.headers_dict)
        return response.json()

    def get_products(self):
        url = f'{self.BASE_URL}/products/'
        response = req.get(url, headers=self.headers_dict)
        return response.json()

    def get_product_by_id(self, productId):
        url = f'{self.BASE_URL}/products/{productId}'
        response = req.get(url, headers=self.headers_dict)
        return response.json()
    
    def get_teams(self):
        teams = []
        domains = self.get_domains()
        for domain in domains:
            domain_id = str(domain.get('domainId'))
            domain_product_teams = self.ext_sbbid_get_domain_teams(domain_id).get('productTeams')
            for domain_product_team in domain_product_teams:
                team_id = str(domain_product_team.get('productTeamId'))
                team_name = str(domain_product_team.get('productTeamName'))
                domain_product_team = {'productTeamId': team_id, 
                                       'productTeamName': team_name, 
                                       'productTeamNameDisplayName': team_id + ' — '+ team_name}
                teams.append(domain_product_team)
        sorted_team_objects = ([x['productTeamNameDisplayName'] for x in sorted(teams, key=lambda k: k['productTeamId'])])
        return sorted_team_objects
