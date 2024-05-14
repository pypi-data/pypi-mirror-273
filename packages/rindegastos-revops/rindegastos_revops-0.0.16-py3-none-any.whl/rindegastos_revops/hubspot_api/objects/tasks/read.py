from ..base_read import BaseRead
from ....hubspot_api.helpers.hubspot import HubspotConnectorApi, Endpoints
from typing import Optional

class Read():
    def __init__(self,
                 client:HubspotConnectorApi, 
                 archived:bool,
                 properties:list):
        
        self.tasks = BaseRead(
            client=client,
            object_endpoint = Endpoints.TASKS,
            archived = archived,
            properties = properties)

    def records(self, test:Optional[bool]):
        object_records = self.tasks.all_pages_df(test)
        return object_records