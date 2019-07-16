# Splunk Cloud SDK for Python

The Splunk Cloud software development kit (SDK) for Python contains library code and examples to enable you to build apps using the Splunk Cloud services with the Python 3 programming language.

To use the Splunk Cloud SDKs, you must be included in the Splunk Investigates Beta Program.
Sign up here: https://si.scp.splunk.com/.

## Terms of Service (TOS)
[Splunk Cloud Terms of Service](https://www.splunk.com/en_us/legal/terms/splunk-cloud-pre-release-terms-of-service.html)

## Get started

The `SplunkCloud` class is the main entry point to the Splunk Cloud SDK for Python.
Instantiate this class for an index of all the Splunk Cloud services. Each service name is a property on the
client object.

```python
from splunk_sdk import Context
from splunk_sdk.auth import PKCEAuthManager
from splunk_sdk.splunk_cloud import SplunkCloud

# Create a test context--you might want to pass more to the context
context = Context(tenant="your_tenant")

# Initialize the auth manager
auth_manager = PKCEAuthManager(client_id="your_client_id",
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
from splunk_sdk import BaseClient, Context
from splunk_sdk.identity import IdentityAndAccessControl
from splunk_sdk.auth import ClientAuthManager

am = ClientAuthManager(client_id="your_client_id", client_secret="your_client_secret")
base_client = BaseClient(context=Context(tenant="your_tenant"), auth_manager=am)
identity = IdentityAndAccessControl(base_client)
identity.validate_token()
```

## Conventions

Most of the service methods for the Splunk Cloud SDK for Python are generated directly from the Splunk Cloud service specifications.
As a result, the functionality should match exactly between code written using the SDK and code that calls the services
directly. The goal of this SDK is to make your code match with Python idioms and conventions,
including using parameters that match Python casing guidelines. For example, when a service specifies an argument as `lastUpdate`,
that field is known as a more Pythonesque `last_update` when used in the Splunk Cloud SDK for Python.

The Splunk Cloud SDK for Python also manages setting up requests, handling authentication, and serializing and deserializing models for requests. If an error occurs in the service, the SDK raises an exception that has properties for why the error
occurred. Every response from a service call results in some subclass of `SSCModel`. Calls that don't return a body
return `SSCVoidModel`, which has a `response` property with access to the raw HTTP response.

## Documentation
For general documentation, see the [Splunk Developer Cloud Portal](https://sdc.splunkbeta.com/).

For reference documentation, see the Splunk Cloud SDK for Python API Reference (_coming soon_). 

## Contributing

Do not directly edit any source file with the prefix `gen_` because it was generated from service specifications.

## Contact
If you have questions, reach out to us on [Slack](https://splunkdevplatform.slack.com) in the **#sdc** channel or email us at _sdcbeta@splunk.com_.
