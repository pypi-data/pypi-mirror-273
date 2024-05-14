from ..helpers.hubspot import HubspotConnectorApi, Endpoints
from ..helpers.get_dataframe import next_page, get_dataframe

from typing import Optional
import pandas as pd
import requests

class BaseRead():
    def __init__(self,
                 client:HubspotConnectorApi, 
                 object_endpoint: Endpoints,
                 archived: bool = False,
                 properties: list = []):
        
        self.client = client
        self.object_endpoint = object_endpoint
        self.archived = archived
        self.properties = properties


    def call(self, after:Optional[str] = None, limit:int = 100) -> requests.Response:
        
        querystring = {"limit":limit,"archived":self.archived,'properties':self.properties}
        if after:
            querystring["after"] = after

        response = requests.request("GET", self.client.endpoint(self.object_endpoint), headers=self.client.headers, params=querystring)

        return response
    
    def all_pages_df(self, test:bool = True) -> Optional[pd.DataFrame]:
        after = None
        dfs = []

        while True:
            rq = self.call(after)
            if rq.status_code == 200:
                df = get_dataframe(rq)
                dfs.append(df)
                after = next_page(rq.json())
                if after == None or test:
                    break
            else:
                return None

        return pd.concat(dfs).reset_index(drop=True)