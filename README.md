# Splunk Cloud Services SDK for Python

The Splunk Cloud Services software development kit (SDK) for Python contains library code and examples to enable you to build apps using the Splunk Cloud Services services with the Python 3 programming language.

## Terms of Service (TOS)

Log in to [Splunk Investigate](https://si.scp.splunk.com/) and accept the Terms of Service when prompted.

## Install the Splunk Cloud Services SDK for Python

To install the Splunk Cloud Services SDK for Python and its dependencies, run the following pip command: 

```
pip install splunk-cloud-sdk 
```

For more about installing the pip package installer, see the [PyPA](https://pypi.org/project/pip/) website.


## Get started

The `SplunkCloud` class is the main entry point to the Splunk Cloud Services SDK for Python.
Instantiate this class for an index of all the Splunk Cloud Services services. Each service name is a property on the
client object.

```python
from splunk_sdk import Context
from splunk_sdk.auth import PKCEAuthManager
from splunk_sdk.splunk_cloud import SplunkCloud

# Create a test context--you might want to pass more to the context
context = Context(host="your_scp_host", tenant="your_tenant")

# Initialize the auth manager
auth_manager = PKCEAuthManager(host="your_auth_host",
                               client_id="your_client_id",
                               username="your_username",
                               password="your_password",
                               redirect_uri="your_app_redirect_uri")

scloud = SplunkCloud(context, auth_manager)
for s in scloud.catalog.list_datasets():
   print(s.name)
```

If you want only a small subset of functionality, you can instantiate services individually
and avoid loading code for services you don't need:

```python
from splunk_sdk.base_client import BaseClient, Context
from splunk_sdk.identity import Identity
from splunk_sdk.auth import ClientAuthManager

auth_manager = ClientAuthManager(host="your_auth_host", client_id="your_client_id", client_secret="your_client_secret")
base_client = BaseClient(context=Context(tenant="your_tenant"), auth_manager=auth_manager)
identity = Identity(base_client)
identity.validate_token()
```

## Conventions

Most of the service methods for the Splunk Cloud Services SDK for Python are generated directly from the Splunk Cloud Services service specifications.
As a result, the functionality should match exactly between code written using the SDK and code that calls the services
directly. The goal of this SDK is to make your code match with Python idioms and conventions,
including using parameters that match Python casing guidelines. For example, when a service specifies an argument as `lastUpdate`,
that field is known as a more Pythonesque `last_update` when used in the Splunk Cloud Services SDK for Python.

The Splunk Cloud Services SDK for Python also manages setting up requests, handling authentication, and serializing and deserializing models for requests. If an error occurs in the service, the SDK raises an exception that has properties for why the error
occurred. Every response from a service call results in some subclass of `SSCModel`. Calls that don't return a body
return `SSCVoidModel`, which has a `response` property with access to the raw HTTP response.

## Versions

Some services will support multiple API versions and designate which one is recommended for most users.
The SDK will default to the recommend version via module remapping and the integration tests will also use this.
In order to choose the non-recommended version of a service you will need to explicitly import that version like this:
```python
from splunk_sdk.action.v1beta2 import *
```

## Documentation
For general documentation, see the [Splunk Developer Portal](https://dev.splunk.com/scs/).

For reference documentation, see the [Splunk Cloud Services SDK for Python API Reference](https://dev.splunk.com/scs/reference/sdk/splunk-cloud-sdk-python/).

## Contributing

Do not directly edit any source file with the prefix `gen_` because it was generated from service specifications.

## Contact
If you have questions, reach out to us on [Slack](https://splunkdevplatform.slack.com) in the **#sdc** channel or email us at _devinfo@splunk.com_.
