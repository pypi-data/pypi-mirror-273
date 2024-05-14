class HarnessPipelines:
    def __init__(self, harness_service):
        self._harness_service = harness_service

    def fetch_pipeline(self, org_identifier, project_identifier, pipeline_identifier):
        endpoint = f"/v1/orgs/{org_identifier}/projects/{project_identifier}/pipelines/{pipeline_identifier}"
        return self._harness_service._make_request("GET", endpoint)
    
    def list_pipelines(self, org_identifier = None, project_identifier = None, params = None):
        endpoint = f"/v1/orgs/{org_identifier}/projects/{project_identifier}/pipelines"
        return self._harness_service._make_request("GET", endpoint, params = params)
    
    def create_pipeline(self, org_identifier, project_identifier, pipeline_data):
        endpoint = f"/v1/orgs/{org_identifier}/projects/{project_identifier}/pipelines"
        return self._harness_service._make_request("POST", endpoint, json=pipeline_data)
    
    def update_pipeline(self, org_identifier, project_identifier, pipeline_data, pipeline_identifier):
        endpoint = f"/v1/orgs/{org_identifier}/projects/{project_identifier}/pipelines/{pipeline_identifier}"
        return self._harness_service._make_request("PUT", endpoint, json=pipeline_data)
    
    def delete_pipeline(self, org_identifier, project_identifier, pipeline_identifier):
        endpoint = f"/v1/orgs/{org_identifier}/projects/{project_identifier}/pipelines/{pipeline_identifier}"
        return self._harness_service._make_request("DELETE", endpoint)