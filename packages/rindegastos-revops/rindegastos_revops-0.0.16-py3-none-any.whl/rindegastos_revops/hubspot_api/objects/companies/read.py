from ..base_read import BaseRead
from ...helpers.hubspot import HubspotConnectorApi, Endpoints
from typing import Optional

class Read():
    def __init__(self,
                 client:HubspotConnectorApi, 
                 archived:bool,
                 properties:list):
        
        self.companies = BaseRead(
            client=client,
            object_endpoint = Endpoints.COMPANIES,
            archived = archived,
            properties = properties)

    def records(self, test:Optional[bool]):
        object_records = self.companies.all_pages_df(test)
        return object_records