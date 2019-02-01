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
    import os
    from splunk_sdk.auth.pkce_auth_manager import PKCEAuthManager
    from splunk_sdk.common.context import Context
    from splunk_sdk.splunk_cloud import SplunkCloud

    # Create a test context, you may want to pass more to the context
    context = Context(host=os.environ.get('SPLUNK_HOST'), api_host=os.environ.get('SPLUNK_API_HOST'), app_host=os.environ.get('SPLUNK_APP_HOST'), tenant=os.environ.get('SPLUNK_TENANT'))

    # Initialize the auth manager
    auth_manager = PKCEAuthManager(host=os.environ.get('SPLUNK_AUTH_HOST'),
                                   client_id=os.environ.get('SPLUNK_APP_CLIENT_ID'),
                                   authz_server=os.environ.get('SPLUNK_APP_SERVER'),
                                   username=os.environ.get('SPLUNK_USERNAME'),
                                   password=os.environ.get('SPLUNK_PASSWORD'),
                                   redirect_uri='http://localhost')

    scloud = SplunkCloud(context, auth_manager)
    for s in scloud.gateway.list_specs():
       print(s.name)

    # Output looks like this
    """
    SCP Example Application
    Collect Service
    KV Store API
    Metadata Catalog
    Metering Service API
    Data Stream Processing REST API
    Identity and Access Control
    Action Service
    """
   ```


## Documentation
For general documentation about the Splunk Cloud SDK for Python, see:
- TODO(dan): update this url https://sdc.splunkbeta.com/docs/sdks

For the API reference for the Splunk Cloud SDK for Go, see:
- https://sdc.splunkbeta.com/reference/sdk/splunk-cloud-sdk-python

The API reference contains detailed information about all classes and functions, with clearly-defined parameters and return types.
