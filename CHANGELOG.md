# Splunk Cloud SDK for Python Changelog

## Version 11.0.0
### Services

#### Breaking Changes

##### Features

- Identity v2beta1:
    - Model `AddInvisibleMemberBody` removed
    - Endpoints `add_invisible_member`, `get_member_admin` and `remove_member_admin` removed

- Provisioner v1beta1
    - Models `CreateProvisionJobBody`, `ProvisionJobInfo`, `ProvisionJobInfoErrors`, `ProvisionJobInfoErrors` and 
    `ProvisionJobs` removed
    - Endpoints `create_provision_job`, `get_provision_job` and `list_provision_jobs` removed

- Streams v3beta1:
    - Models `CollectJobPatchRequest`, `CollectJobRequest`, `CollectJobResponse`, `CollectJobStartStopResponse`, 
    `EntitlementRequest`, `EntitlementResponse`, `PaginatedResponseOfCollectJobResponse`, `PaginatedResponseOfPlugin`, 
    `PaginatedResponseOfRulesResponse`,  `PaginatedResponseOfRuleKind`, `Plugin`, `PluginPatchRequest`, `PluginRequest`, 
    `PluginResponse`, `RulesRequest` and `RulesResponse` removed

    - Model `UploadFile` renamed to `UploadFileResponse`

    - Endpoints `create_collect_job`, `create_rules_package`, `delete_collect_jobs`, `delete_collect_job`, `delete_entitlements`, 
    `delete_plugin`, `delete_rules_package`, `get_collect_job`, `get_entitlements`, `get_plugins`, `get_rules_package_by_id`, 
    `list_collect_jobs`, `list_rules_kinds`, `list_rules_packages`, `patch_plugin`, `register_plugin`, `release_info`, 
    `set_entitlements`, `start_collect_job`, `stop_collect_job`, `update_collect_job`, `update_plugin` and `update_rules_package_by_id` 
    removed  

#### Non-Breaking Changes

##### Features

- Identity v2beta1:
    - New model `CreatePrincipalBody` added
    - New endpoint `create_principal` added

- Identity v3: 
    - New version introduced

- Identity v3alpha1
    - New models `GroupMemberList` and `GroupRoleList`added

- Ingest v1beta2: 
    - New endpoints `post_collector_raw` and `post_collector_raw_v1` added

- Streams v2beta1:
    - New property `attributes` added to `ConnectorResponse`
    - New property `status_description` added to `PipelineReactivateResponse`
    - New parameter `functionOp`added to `listConnections`

- Streams v3beta1
    - New model `UploadFileResponse` added
    - New endpoint `delete_lookup_file`, `get_lookup_file_metadata` and `get_lookup_files_metadata` added

## Version 10.0.0

### Services

#### Breaking Changes

##### Features

- Catalog v2beta1:
    - `create_dataset_import` returns datatype of `Dataset` (replaced 'ImportDataset')
    - `create_dataset_import_by_id` returns `DatasetImportedby` (replaced 'ImportDataset')
    - `DatasetImportedBy` has a new property `owner` and property `name` is now optional

- Identity service v2beta1:
    - Models `AppList`, `GroupList`, `Keylist`, `MemberList`, `PricipalList`, `RoleList`, `RolePermissionList` and `SubscriptionList` removed
    - Property `encode_state` added to `ResolveBody` model
    - Property `count` removed from model `IdentityProviderList`
    - Property `name` removed from model `SenstiveTenant`
    - Properties `count` and `details` removed from models `ServiceAccountList`, `TakedownPrincipalList`, `TenantList`
    - Property `items` in model `ServiceAccountList` has a reference to `ServiceAccount`
    - Property `items` in model `TakedownPrincipalList` has a reference to `TakedownPrincipal`
    - Property `items` in model `TenantList` has a reference to `Tenant`

- Ingest v1beta2: 
    - New properties `ack_enabled`, `allow_query_string_auth`, `diabled` and `indexes` added to models `HecTokenAccessResponse`, `HecTokenCretaeRequest`, `HecTokenCreateResponse`, `HecTokenUpdateRequest`
    - Remove endpoint of `upload_files`

- Provisioner v1beta1:
    - Model `ECStackName` renamed to `EcStackName`

- Search v2beta1:
    - Model `ListSearchResultsResponseFields` renamed to `ListPreiviewResultsResponseFields`

- Search v3alpha1:
    - Model `ListSearchResultsResponseFields` renamed to `ListPreiviewResultsResponseFields`

- Stream v3beta1: 
    - Model `RulesSourcetypesResponse` renamed to `RulesPackageSourcetypes`
    - Model `RulesActionsResponse` renamed to `RulesPackageActions`
    
#### Non-Breaking Changes

##### Features

- Auth 
    - `ServicePrincipalAuthManager` added to Auth service

- Identity v2beta1:
    - New model `AddInvisibleMemberBody` added
    - New endpoints `add_invisible_member`, `get_member_admin` and `remove_member_admin` added
    - New properties `expires_at` and `visible` added to `Member` model
    - New models `DeviceAuthInfo` and `UpdateRoleBody` added

- Identity v3alpha1: 
    - New version introduced

- Ingest v1beta2: 
    - New models `UploadSuccessResponse` and `FileUploadDetails`  added

- KVStore v1beta1:
    - New endpoint `truncate_records` added

- Search v3alpha1:
    - New models `SearchModule`, `StatementDispatchStatus`, and `SingleSatatementQueryParamters` added
    - New endpoints `create_multi_search_method` and `create_search_statements` added

- Streams v2beta1:
    - New property `messages` added to model `ConnectionSaveResponse`
    - New property `complexity` added to model `PipelineResponse`
    - New property `activate_latest_version` added to model `ReactivatePipelineRequest`

- Streams v3beta1:
    - New models `CollectJobPatchRequest`, `DataStream`, `DataStreamRequest`, `DataStreamResponse`, `EntitlementRequest`,
     `EntitlementResponse`, `PaginatedResponseOfRuleKind`, `RulesKind` and `PluginResponse`
    - New endpoints `create_data_stream`, `delete_collect_job`, `delete_data_stream`, `delete_entitlements`, `delete_rules_package`, 
     `describe_data_stream`, `get_entitlements`, `get_rules_package_by_id`, `list_data_streams`, `list_rule_kinds`, `release_info`, 
     `set_entitlements`, `update_collect_job`, `update_data_stream` and `update_rules_package_by_id` added

## Version 9.0.0

### Library

#### Breaking Changes
- App Registry
	- `WebAppFromAppResponseGetList` has been removed
	- `WebAppPOST`  has been removed

##### Features
- Catalog
	- `extract_fields` has been added
- Search
    - `extract_fields` has been added
- Streams
    - `PaginatedResponseOfCollectJobResponse` has been added
    - `RulesResponse` has been added
    - `RulesSourcetypesResponse` has been added
    - `RulesActionsResponse` has been added
    - `PaginatedResponseOfRulesResponse` has been added
    - `PaginatedResponseOfRulesResponse` has been added
    - `RulesRequest` has been added
    
### Services

#### Breaking Changes
- AppRegistry
	- Removed support for creating app of type `WebApp`,  
	
##### Features
- Streams
    - New endpoints for `CreateRulesPackage`, `GetRulesPackage`, `ListRulesPackage`, `ListCollectJobs` have been added


## Version 8.0.0

#### Breaking Changes
- Catalog service v2beta1: get_dataset, get_dataset_by_id and list_datasets endpoints now return data type of DatasetGet instead of Dataset
- Identify service v2beta1: remove endpoint of set_principal_public_keys

- Kvstore service v1beta1: insert_records endpoint has a new parameter of allow_updates

- Stream service v3beta1: 
    - Remove endpoint: uploadPlugin
    - reactivate_pipeline  has a new parameter of reactivate_pipeline_request


#### Non-Breaking Changes
- Identify service v2beta1: 
    - new endpoints added: add_principal_public_key, get_principal_public_key, get_principal_public_keys, delete_principal_public_key, and update_principal_public_key 

- Stream service v3beta1: 
    - new endpoints added: startCollectJob,stopCollectJob


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