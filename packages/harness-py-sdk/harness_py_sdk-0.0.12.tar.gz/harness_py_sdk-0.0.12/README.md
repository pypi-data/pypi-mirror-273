# Harness Python SDK

Welcome to the Harness Python SDK! This SDK provides a convenient way to interact with the Harness platform's APIs using Python.

## Prerequisites

Before using the SDK, ensure you have the following:

- **Harness Platform API Key**: You'll need an API key to authenticate with the Harness API. You can [create a personal API key](https://developer.harness.io/docs/platform/automation/api/add-and-manage-api-keys/#create-personal-api-keys-and-tokens).
- **Python 3 or higher**: This SDK requires Python 3 or higher to run.
- **Account Identifier**: The account identifier is required for authenticating with the Harness API. You can find this identifier in the URL when you're logged into your Harness account. For example, in the URL `https://app.harness.io/ng/account/Fak3Acc0unt1D/settings/overview`, the account identifier is `Fak3Acc0unt1D`.

Install the SDK using the following command:

```bash
pip install harness-py-sdk
```

## Getting Started

To get started with the SDK, you'll need to authenticate with the Harness API. Here's how you can do it:

```python
import os
from harness_py_sdk import sdk

harness_service = sdk.HarnessService(os.environ.get('HARNESS_PLATFORM_API_KEY'), "my-account-identifier")
```

### Example 1 - Listing Services

Use the following code to list all services:

```python
harness_service.services.fetch_services()
```

### Example 2 - Listing Connectors using the old API

To list connectors using the old API, use the following code:

```python
harness_service.connectors.old.fetch_connectors_listV2(
    data={
        "types": ["HttpHelmRepo"],
        "filterType": "Connector"
    },
    org_identifier=org_identifier,
    project_identifier=project_identifier
)
```

## Reference

Here's a reference to the available classes in the SDK:

- **Connectors**: [Documentation](https://guilhermezanini-harness.github.io/harness-py-sdk/harness_py_sdk/harness_connectors.html)
- **Old Connectors**: [Documentation](https://guilhermezanini-harness.github.io/harness-py-sdk/harness_py_sdk/harness_old_connectors.html)
- **Pipelines**: [Documentation](https://guilhermezanini-harness.github.io/harness-py-sdk/harness_py_sdk/harness_pipelines.html)
- **Services**: [Documentation](https://guilhermezanini-harness.github.io/harness-py-sdk/harness_py_sdk/harness_services.html)
- **Templates**: [Documentation](https://guilhermezanini-harness.github.io/harness-py-sdk/harness_py_sdk/harness_templates.html)
