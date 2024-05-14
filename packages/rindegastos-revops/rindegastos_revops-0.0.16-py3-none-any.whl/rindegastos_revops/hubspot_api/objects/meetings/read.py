from ..base_read import BaseRead
from ....hubspot_api.helpers.hubspot import HubspotConnectorApi, Endpoints
from typing import Optional

class Read():
    def __init__(self,
                 client:HubspotConnectorApi, 
                 archived:bool,
                 properties:list):
        
        self.meetings = BaseRead(
            client=client,
            object_endpoint = Endpoints.MEETINGS,
            archived = archived,
            properties = properties)

    def records(self, test:Optional[bool]):
        object_records = self.meetings.all_pages_df(test)
        return object_records