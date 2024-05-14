
from .harness_old_connectors import HarnessOldConnectors

class HarnessConnectors():
    def __init__(self, harness_service):
        self._harness_service = harness_service
        self._old = None  # Placeholder for the Old Connector class

    @property
    def old(self):
        if self._old is None:
            self._old = HarnessOldConnectors(self.harness_service)  # Initialize with self to pass the session
        return self._old
    
    def fetch_connector(self, identifier, org_identifier=None, project_identifier=None):
        """Retrieves the information of the connector with the matching connector identifier.
        Args:
            identifier (str): Connector identifier
            org_identifier (str): Organization identifier
            project_identifier (str): Project identifier
        """
        endpoint = self.harness_service._construct_url("connectors", identifier, org_identifier, project_identifier)
        return self.harness_service._make_request("GET", endpoint)
    
    def fetch_connectors(self, org_identifier=None, project_identifier=None):
        endpoint = self.harness_service._construct_url("connectors", None, org_identifier, project_identifier)
        return self.harness_service._make_request("GET", endpoint)
    
    def update_connector(self, identifier, data, org_identifier=None, project_identifier=None):
        endpoint = self.harness_service._construct_url("connectors", identifier, org_identifier, project_identifier)
        return self.harness_service._make_request("PUT", endpoint, json=data)