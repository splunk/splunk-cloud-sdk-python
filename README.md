# splunk-cloud-sdk-python
A Python 3 client for Splunk Cloud services

# Terms of Service (TOS)
[Splunk Cloud Terms of Service](https://www.splunk.com/en_us/legal/terms/splunk-cloud-pre-release-terms-of-service.html)

# Getting started
---

## Install Python 3 and Python tools
[OS Specific Instructions](https://realpython.com/installing-python/)

1. Install Python 3.7.0 or later with pip3.

    ```bash
    # Mac OS X
    $ brew install python3
    ```

2. Optionally install virtualenv and configure it

    ```bash
    $ virtualenv --python=python3 .venv

    # activate your virtualenv
    $ . .venv/bin/activate

    # Install the python sdk into your virtualenv
    (.venv)$ pip install splunk-cloud-sdk-python-<version>.tar.gz

    # deactivate your virtualenv
    (.venv)$ deactivate
    ```


## Using the splunk-cloud-sdk-python from your python project
   ```python

   from splunk_sdk.auth.pkce_auth_manager import PKCEAuthManager
   from splunk_sdk.common.context import Context
   from splunk_sdk.gateway.client import Gateway
   from splunk_sdk.service_client import get_client

   # Create a test context, you may want to pass more to the context
   context = Context(host=<host>, api_host=<api_host>, app_host=<app_host>, port=<443>, scheme=<'https'>, tenant=<tenant>)

   # Initialize the auth manager
   auth_manager = PKCEAuthManager(host=<host>
                                  client_id=<client_id>,
                                  server=<server>,
                                  username=<username>,
                                  password=<password>,
                                  redirect_uri=<redirect_uri>)

   # Get an instance of the service client
   service_client = get_client(context, auth_manager)

   # Get an instance of the Gateway client
   gateway = Gateway(self.service_client, cluster='api')

   # List all the specs in the api cluster
   for s in gateway.list_specs():
       print(s.name)

   # Output looks like this
   """
   Identity and Access Control
   Splunk Search Service
   Ingest API
   Action Service
   Data Stream Processing REST API
   Splunk Forwarder Service
   KV Store API
   Metadata Catalog
   Ingest API
   Metering Service API
   Splunk Forwarder Service
   Collect Service
   """

   ```



## Documentation
For general documentation about the Splunk Cloud SDK for Python, see:
- TODO(dan): update this url https://sdc.splunkbeta.com/docs/sdks

For the API reference for the Splunk Cloud SDK for Go, see:
- https://sdc.splunkbeta.com/reference/sdk/splunk-cloud-sdk-python

The API reference contains detailed information about all classes and functions, with clearly-defined parameters and return types.
