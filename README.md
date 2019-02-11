# Splunk Cloud SDK for Python

**Version 0.0.1**

The Splunk Cloud Software Development Kit (SDK) for Python 3 contains library code and examples designed to enable developers to build applications using the Splunk Cloud services.

## Terms of Service
[Splunk Cloud Terms of Service](https://www.splunk.com/en_us/legal/terms/splunk-cloud-pre-release-terms-of-service.html)

## Install Python 3 and Python tools

1. Install Python 3.7.0 or later. For operating system-specific instructions, see [Python 3 Installation & Setup Guide](https://realpython.com/installing-python/).

    For example, to install Python 3 on macOS, enter the following at the command line: 
    
    ```bash
    # Install Python 3 using Pip 3
    $ brew install python3
    ```

2. Optionally, install and configure [Virtualenv](https://virtualenv.pypa.io/en/latest/).

    For example, to install Virtualenv on macOS, enter the following at the command line: 
    
    ```bash
    $ virtualenv --python=python3 .venv

    # Activate your virtualenv
    $ . .venv/bin/activate

    # Install the Splunk Cloud SDK for Python SDK your virtualenv
    (.venv)$ pip install splunk-cloud-sdk-python-<version>.tar.gz

    # Deactivate your virtualenv
    (.venv)$ deactivate
    ```


## Use the Splunk Cloud SDK for Python

The following example shows how to use the Splunk Cloud SDK for Python from your Python project. 

   ```python
    import os
    from splunk_sdk.auth.pkce_auth_manager import PKCEAuthManager
    from splunk_sdk.common.context import Context
    from splunk_sdk.splunk_cloud import SplunkCloud

    # Create a test context--you might want to pass more to the context
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

For more information, see the Splunk Developer Cloud Portal: 
-   [Developer Guide](https://sdc.splunkbeta.com/docs/) contains general documentation about working with Splunk Developer Cloud.
-   [Splunk Cloud SDK for Python API Reference](https://sdc.splunkbeta.com/reference/sdk/splunk-cloud-sdk-python) contains detailed information about classes, functions, parameters, and return types.

## Contact
If you have questions, reach out to us on [Slack](https://splunkdevplatform.slack.com) in the **#sdc** channel or email us at _sdcbeta@splunk.com_.
