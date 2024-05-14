import requests

from .harness_pipelines import HarnessPipelines
from .harness_connectors import HarnessConnectors
from .harness_services import HarnessServices
from .harness_templates import HarnessTemplates

class HarnessService:
    def __init__(self, api_key, account_identifier):
        self._session = requests.Session()
        self._session.   headers.update({
            'x-api-key': api_key,
            'Harness-Account': account_identifier,
            'Content-Type': 'application/json'
        })
        self._account_identifier = account_identifier
        self.base_url = "https://app.harness.io"
        self._pipelines = None  # Placeholder for the Pipelines class
        self._connectors = None  # Placeholder for the Connectors class
        self._services = None  # Placeholder for the Services class
        self._templates = None  # Placeholder for the Templates class

    @property
    def pipelines(self):
        if self._pipelines is None:
            self._pipelines = HarnessPipelines(self)  # Initialize with self to pass the session
        return self._pipelines

    @property
    def services(self):
        if self._services is None:
            self._services = HarnessServices(self)  # Initialize with self to pass the session
        return self._services


    @property
    def templates(self):
        if self._templates is None:
            self._templates = HarnessTemplates(self)  # Initialize with self to pass the session
        return self._templates

    @property
    def connectors(self):
        if self._connectors is None:
            self._connectors = HarnessConnectors(self)  # Initialize with self to pass the session
        return self._connectors

    def _make_request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        response = self._session.request(method, url, **kwargs)
        if response.ok:
            return response.json()
        print(response.text)
        response.raise_for_status()
    
    def _construct_url(self, entity, identifier=None, org_identifier=None, project_identifier=None, identify_scope=False):
        """
        Constructs a URL by appending various identifiers based on the provided scope.
        
        :param entity: Main entity for the URL.
        :param identifier: Optional specific identifier for the entity.
        :param org_identifier: Organization identifier.
        :param project_identifier: Project identifier.
        :param identify_scope: Flag to determine if scope should be dynamically identified.
        :return: Constructed URL as a string.
        """
        parts = ["/v1"]
        
        if identify_scope:
            identifier_scope = self.identify_dynamically_scope(identifier)
            if identifier_scope in ("org", "project"):
                parts.extend(["orgs", org_identifier])
                if identifier_scope == "project":
                    parts.extend(["projects", project_identifier])
        else:
            if org_identifier:
                parts.extend(["orgs", org_identifier])
                if project_identifier:
                    parts.extend(["projects", project_identifier])

        parts.append(entity)

        if identifier:
            if identifier.startswith("org"):
                parts.append(identifier[4:])  # Assumes 'org.' prefix is exactly 4 characters long
            elif identifier.startswith("account"):
                parts.append(identifier[8:])  # Assumes 'account.' prefix is exactly 8 characters long
            else:
                parts.append(identifier)

        return "/".join(parts)
    
    def identify_dynamically_scope(self, identifier):
        if identifier.startswith("org"):
            return "org"
        elif identifier.startswith("account"):
            return "account"
        else:
            return "project"

