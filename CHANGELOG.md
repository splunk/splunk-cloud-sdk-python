# Splunk Cloud SDK for Python Changelog

## Version 5.0.0

### Library

#### Breaking Changes

- Class collisions are now properly disambiguated.
	- AppRegistry
	  - WebApp -> [WebAppFromAppResponseCreateUpdate, WebAppFromAppResponseGetList]
		- ServiceApp -> [ServiceAppFromAppResponseCreateUpdate, ServiceAppFromAppResponseGetList]
		- NativeApp -> [NativeAppFromAppResponseCreateUpdate, NativeAppFromAppResponseGetList]
	- Catalog
		- AliasAction -> [AliasActionFromAction, AliasActionFromActionPOST]
		- AutoKVAction -> [AutoKVActionFromAction, AutoKVActionFromActionPOST]
		- EvalAction -> [EvalActionFromAction, EvalActionFromActionPOST]
		- LookupAction -> [LookupActionFromAction, LookupActionFromActionPOST]
		- RegexAction -> [RegexActionFromAction, RegexActionFromActionPOST]
  - Previously, code generation failed to correctly generate discriminator-based subclasses. This caused returned objects to have missing properties associated with those subclasses.
	- Bugs associated with this issue related to `Dict` conversion have been fixed.

### Services

#### Breaking Changes

- Provisioner
	- Removed endpoints: `CreateEntitlementsJob` and `GetEntitlementsJob`

#### Features

- Ingest
  - Support for new operations: `deleteAllCollectorTokens`, `listCollectorTokens`, `postCollectorTokens`, `deleteCollectorToken`, `getCollectorToken`, `putCollectorToken`
- Search
  - Support for new operation: `deleteJob`

## Version 4.0.0

### Breaking Changes

- AppRegistry
	- Models `AppResponseCreateUpdate`, `AppResponseGetList`, `CreateAppRequest` have been refactored from single models encompassing all app-related properties to discriminator-based app-kind-specific models:  `NativeApp/NativeAppPOST`, `ServiceApp/ServiceAppPOST`, and  `WebApp/WebAppPOST`.
- Catalog
	- `JobDatasetPATCH` and `JobDatasetPOST` have been removed.
- Forwarders
	- `Certificates` model now requires `pem` property.

### Features

- Collect
	- Support for new endpoints: `CreateExecution`, `GetExecution`, `PatchExecution` for scheduled jobs
- Identity
	- New Enum value for TenantStatus: `tombstones`
	- `ListGroups` now allows passing a query  to filter by access permission
	- `ListMemberPermissions` returns new `max-age` header describing how long member permission can be cached
	- New `RevokePrincipalAuthTokens` revokes all tokens for a principal
- Provisioner
  - Support for new endpoints: `CreateEntitlementsJob` and `GetEntitlementsJob`

## Version 3.3.0

### Features

- **search:** Added `filter` parameter to search list_jobs endpoint

## Version 3.2.0

### Features

- **ml:** added `INITIALIZING` value to `StatusEnum` model ([a3ef356](https://github.com/splunk/splunk-cloud-sdk-python/commit/a3ef356))

## Version 3.1.0

### Non-breaking Changes

- Update PKCE auth flow to read the CSRF token from the response cookie returned from the /csrfToken endpoint to mitigate security bug SCP-16944

## Version 3.0.0

### Breaking Changes

- **streams:** Remove ALREADYACTIVATEDWITHCURRENTVERSION from Pipeline_reactivation_statusEnum ([c36f5c9](https://github.com/splunk/splunk-cloud-sdk-python/commits/c36f5c9))
- **streams:** Remove optional create_user_id field on PipelineRequest ([c36f5c9](https://github.com/splunk/splunk-cloud-sdk-python/commits/c36f5c9))

### Non-breaking Changes

- **search:** Expose optional required_freshness field on SearchJob class ([c36f5c9](https://github.com/splunk/splunk-cloud-sdk-python/commits/c36f5c9))
- **streams:** Expose NOTACTIVATED on Pipeline_reactivation_statusEnum ([c36f5c9](https://github.com/splunk/splunk-cloud-sdk-python/commits/c36f5c9))

## Version 2.0.0

### Non-Breaking Changes

- Regenerated all client bindings
- Fix catalog call for create dashboard annotation using AnnotationPOST

### Breaking Changes

- Action ScalePolicy is now an object
