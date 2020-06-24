# Splunk Cloud SDK for Python Changelog

## Version 7.0.0

### Library

#### Breaking Changes

#### Non-Breaking Changes
- App Registry
	- `NativeAppFromAppResponseCreateUpdate` has been added
	- `NativeAppFromAppResponseGetList` has been added
	- `NativeAppPOST`  has been added
	- `ServiceAppFromAppResponseCreateUpdate`  has been added
	- `ServiceAppFromAppResponseGetList` has been added
	- `ServiceAppPOST`  has been added
- Collect
	- `Execution` has been added
	- `ExecutionConflictError` has been added
	- `ExecutionPath` has been added
	- `SingleExecutionResponse` has been added
- Ingest
	- `HECResponse` has been added
	- `HECTokenAccessResponse` has been added
	- `HECTokenCreateRequest` has been added
	- `HECTokenCreateResponse` has been added
	- `HECTokenUpdateRequest` has been added

### Service

####  Breaking Changes
- Streams
	- In v3beta1:
		- Modified `connector_id` parameter to type List[str] in `List_connections` endpoint  

#### Non-Breaking Changes
- Catalog
	- In v2beta1:
		- `AppClientIDProperties` model has been added

- Identity
	- In v2beta1:
		- Added `scope_filter` parameter to  `list_member_permissions ` endpoint 
		- New `Set_principale_public_keys` endpoint

- Search
	- In v2beta:
		- Float typed parameter changed to Int for endpoints: `List_events_summary`, `List_jobs`, `List_preview_results` `list_results`

- Streams
	- New `get_file_metadata` endpoint

- New feature
	- 429 Retry Handling


## Version 6.0.0

### Services

#### Breaking Changes

##### Features
- Streams
    - A new version of spec: v3beta1 has been added. Changes in the new version:
      - `CompileDSL` is not longer supported, substituted by Compile which leverages SPL instead of DSL to produce streams JSON object
      - CRUD on `Group` endpoints have been removed and all models corresponding to Groups have been removed
      - `ExpandGroup` which creates and returns the expanded version of a group has been removed
      - `UplPipeline` model replaced by `Pipeline` model
      - `UplNode` model replaced by `PipelineNode` model
      - `UplEdge` model replaced by `PipelineEdge` model
	  - `UplRegistry` model replaced by `RegistryModel` model
	  - `UplFunction` model replaced by `FunctionalModel` model
	  - `UplArgument` model replaced by `ArgumentModel` model
	  - `UplCategory` model has been removed
	  - `MergePipelines` support has been removed
	  - `PipelinesMergeRequest` model has been removed
	  - `PipelineDeleteResponse` model has been removed
	  - `DslCompilationRequest` model has been removed
	  - `ObjectNode`model has been removed
    - The default version changed from v2beta1.2 to v3beta1.1
    
#### Non-Breaking Changes

##### Features
- Search 
    - In v2beta1 spec version:
      - Support for new endpoint: `DeleteSearchJob` has been added
	  - New `DeleteSearchJob` creates a search job that deletes events from an index.
- Streams
    - In v2beta1 spec version:
      - Models `GroupFunctionArguments`, `GroupFunctionMappings`, `PipelineMigrationInfo`, `PipelineUpgradeResponse` have been added.
    - In v3beta1 spec version:
      - Models `FilesMetaDataResponse`, `LookupTableResponse`, `ErrorResponse`, `RuleMetrics` have been added.
	  - New `GetLookupTable` endpoint returns lookup table results
	  - New `Decompile` endpoint decompiles UPL and returns SPL 
	  - New `DeleteFile` endpoint deletes a file give a file-id
	  - New `GetFilesMetaData` endpoint returns files metadata

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
