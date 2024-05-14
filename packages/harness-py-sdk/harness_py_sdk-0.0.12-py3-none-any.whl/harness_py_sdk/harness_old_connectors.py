class HarnessOldConnectors():
    def __init__(self, harness_service):
        self._harness_service = harness_service
    
    def fetch_connectors_listV2(self, data, org_identifier=None, project_identifier=None):
        endpoint = "/ng/api/connectors/listV2"
        query_params = {
            "accountIdentifier": self._harness_service._account_identifier,
        }

        if org_identifier:
            query_params["orgIdentifier"] = org_identifier
        
        if project_identifier:
            query_params["projectIdentifier"] = project_identifier

        return self._harness_service._make_request("POST", endpoint, params = query_params, json = data)
    
    def update_connector(self, data, org_identifier=None, project_identifier=None):
        endpoint = "/ng/api/connectors"
        query_params = {
            "accountIdentifier": self._harness_service._account_identifier,
        }

        if org_identifier:
            query_params["orgIdentifier"] = org_identifier
        
        if project_identifier:
            query_params["projectIdentifier"] = project_identifier

        return self._harness_service._make_request("PUT", endpoint, params = query_params, json = data)

