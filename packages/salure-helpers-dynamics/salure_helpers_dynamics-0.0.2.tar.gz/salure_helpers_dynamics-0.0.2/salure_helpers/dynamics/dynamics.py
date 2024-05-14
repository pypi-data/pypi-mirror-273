from salure_helpers.salureconnect import SalureConnect
from typing import Union, List
import requests


class Dynamics(SalureConnect):
    def __init__(self, label: Union[str, List]):
        super().__init__()
        credentials = self.get_system_credential(system='dynamics-365', label=label)
        self.client_id = credentials['client_id']
        self.client_secret = credentials['client_secret']
        self.resource = credentials['resource']
        self.tenant = credentials['tenant_id']
        self.headers = {'authorization': f'Bearer {self.get_access_token()}'}

    def get_access_token(self):
        url = f"https://login.microsoftonline.com/{self.tenant}/oauth2/token"
        payload = {'grant_type': 'client_credentials',
                   'client_id': self.client_id,
                   'client_secret': self.client_secret,
                   'resource': self.resource}
        response = requests.request("POST", url, data=payload)
        return response.json()['access_token']

    def get_data(self, endpoint: str, params: dict = None) -> pd.DataFrame:
        url = f'{self.resource}/data/{endpoint}'
        df = pd.DataFrame()

        while True:
            response = requests.get(url, headers=self.headers, params=params)
            df = pd.concat([df, pd.DataFrame(response.json()['value'])], ignore_index=True)

            if '@odata.nextLink' in response.json():
                url = response.json()['@odata.nextLink']
                params = None
            else:
                break

        return df


