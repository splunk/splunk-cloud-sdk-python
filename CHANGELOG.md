# Splunk Cloud SDK for Python Changelog

## Version 3.3.0
### Features
* **search:** Added `filter` parameter to search list_jobs endpoint

## Version 3.2.0
### Features
* **ml:** added `INITIALIZING` value to `StatusEnum` model ([a3ef356](https://github.com/splunk/splunk-cloud-sdk-python/commit/a3ef356))

## Version 3.1.0
### Non-breaking Changes
* Update PKCE auth flow to read the CSRF token from the response cookie returned from the /csrfToken endpoint to mitigate security bug SCP-16944 

## Version 3.0.0
### Breaking Changes
* **streams:** Remove ALREADYACTIVATEDWITHCURRENTVERSION from Pipeline_reactivation_statusEnum ([c36f5c9](https://github.com/splunk/splunk-cloud-sdk-python/commits/c36f5c9))
* **streams:** Remove optional create_user_id field on PipelineRequest ([c36f5c9](https://github.com/splunk/splunk-cloud-sdk-python/commits/c36f5c9))

### Non-breaking Changes
* **search:** Expose optional required_freshness field on SearchJob class ([c36f5c9](https://github.com/splunk/splunk-cloud-sdk-python/commits/c36f5c9))
* **streams:** Expose NOTACTIVATED on Pipeline_reactivation_statusEnum ([c36f5c9](https://github.com/splunk/splunk-cloud-sdk-python/commits/c36f5c9))

## Version 2.0.0
### Non-Breaking Changes
* Regenerated all client bindings
* Fix catalog call for create dashboard annotation using AnnotationPOST

### Breaking Changes
* Action ScalePolicy is now an object