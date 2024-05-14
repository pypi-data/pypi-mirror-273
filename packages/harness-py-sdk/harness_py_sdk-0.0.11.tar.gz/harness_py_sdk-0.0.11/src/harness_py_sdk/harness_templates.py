class HarnessTemplates():
    def __init__(self, harness_service):
        self._harness_service = harness_service

    def fetch_template_yaml(self, template_identifier, version, org_identifier=None, project_identifier=None):
        endpoint = self._harness_service._construct_url("templates", template_identifier, org_identifier, project_identifier) + f"/versions/{version}"
        return self._harness_service._make_request("GET", endpoint)
    
    def fetch_stable_template_yaml(self, template_identifier, org_identifier=None, project_identifier=None):
        endpoint = self._harness_service._construct_url("templates", template_identifier, org_identifier, project_identifier, identify_scope=True)
        return self._harness_service._make_request("GET", endpoint)
    
    def create_template_pipeline(self, template_data, org_identifier=None, project_identifier=None):
        return self._harness_service._make_request(
            "POST", 
            self._harness_service._construct_url(entity = "templates", org_identifier = org_identifier, project_identifier = project_identifier), 
            json=template_data
        )