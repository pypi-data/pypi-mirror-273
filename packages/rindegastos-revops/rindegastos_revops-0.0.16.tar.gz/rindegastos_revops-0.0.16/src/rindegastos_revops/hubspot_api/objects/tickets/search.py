from ..base_search import BaseSearch
from ....hubspot_api.helpers.hubspot import HubspotConnectorApi, Endpoints

from datetime import datetime


class Search():
    def __init__(self,
                 client:HubspotConnectorApi, 
                 from_date:datetime, 
                 to_date:datetime, 
                 property_filter:str = "createdate"):
        
        self.calls_search = BaseSearch(
            client=client,
            properties_endpoint = Endpoints.PROPERTIES_TICKETS,
            object_endpoint = Endpoints.TICKETS_SEARCH,
            property_filter = property_filter,
            from_date = from_date,
            to_date = to_date
        )


    def records(self):
        object_records = self.calls_search.all_pages_df()
        return object_records