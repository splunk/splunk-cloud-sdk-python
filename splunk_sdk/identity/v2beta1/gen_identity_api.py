# coding: utf-8

# Copyright © 2021 Splunk, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# [http://www.apache.org/licenses/LICENSE-2.0]
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

############# This file is auto-generated.  Do not edit! #############

"""
    SDC Service: Identity

    With the Identity service in Splunk Cloud Services, you can authenticate and authorize Splunk Cloud Services users.

    OpenAPI spec version: v2beta1.20 
    Generated by: https://openapi-generator.tech
"""


from requests import Response
from string import Template
from typing import List, Dict

from splunk_sdk.base_client import handle_response
from splunk_sdk.base_service import BaseService
from splunk_sdk.common.sscmodel import SSCModel, SSCVoidModel

from splunk_sdk.identity.v2beta1.gen_models import AddGroupMemberBody
from splunk_sdk.identity.v2beta1.gen_models import AddGroupRoleBody
from splunk_sdk.identity.v2beta1.gen_models import AddMemberBody
from splunk_sdk.identity.v2beta1.gen_models import CreateGroupBody
from splunk_sdk.identity.v2beta1.gen_models import CreatePrincipalBody
from splunk_sdk.identity.v2beta1.gen_models import CreateRoleBody
from splunk_sdk.identity.v2beta1.gen_models import ECJwk
from splunk_sdk.identity.v2beta1.gen_models import Group
from splunk_sdk.identity.v2beta1.gen_models import GroupMember
from splunk_sdk.identity.v2beta1.gen_models import GroupRole
from splunk_sdk.identity.v2beta1.gen_models import IdentityProviderBody
from splunk_sdk.identity.v2beta1.gen_models import IdentityProviderConfigBody
from splunk_sdk.identity.v2beta1.gen_models import Member
from splunk_sdk.identity.v2beta1.gen_models import Principal
from splunk_sdk.identity.v2beta1.gen_models import PrincipalPublicKey
from splunk_sdk.identity.v2beta1.gen_models import PrincipalPublicKeyStatusBody
from splunk_sdk.identity.v2beta1.gen_models import Role
from splunk_sdk.identity.v2beta1.gen_models import RolePermission
from splunk_sdk.identity.v2beta1.gen_models import ValidateInfo


class Identity(BaseService):
    """
    Identity
    Version: v2beta1.20
    With the Identity service in Splunk Cloud Services, you can authenticate and authorize Splunk Cloud Services users.
    """

    def __init__(self, base_client):
        super().__init__(base_client)

    def add_group_member(self, group: str, add_group_member_body: AddGroupMemberBody, query_params: Dict[str, object] = None) -> GroupMember:
        """
        Adds a member to a given group.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "group": group,
        }

        path = Template("/identity/v2beta1/groups/${group}/members").substitute(path_params)
        url = self.base_client.build_url(path)
        data = add_group_member_body.to_dict()
        response = self.base_client.post(url, json=data, params=query_params)
        return handle_response(response, GroupMember)

    def add_group_role(self, group: str, add_group_role_body: AddGroupRoleBody, query_params: Dict[str, object] = None) -> GroupRole:
        """
        Adds a role to a given group.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "group": group,
        }

        path = Template("/identity/v2beta1/groups/${group}/roles").substitute(path_params)
        url = self.base_client.build_url(path)
        data = add_group_role_body.to_dict()
        response = self.base_client.post(url, json=data, params=query_params)
        return handle_response(response, GroupRole)

    def add_member(self, add_member_body: AddMemberBody, query_params: Dict[str, object] = None) -> Member:
        """
        Adds a member to a given tenant.
        """
        if query_params is None:
            query_params = {}

        path_params = {
        }

        path = Template("/identity/v2beta1/members").substitute(path_params)
        url = self.base_client.build_url(path)
        data = add_member_body.to_dict()
        response = self.base_client.post(url, json=data, params=query_params)
        return handle_response(response, Member)

    def add_principal_public_key(self, principal: str, ec_jwk: ECJwk, query_params: Dict[str, object] = None) -> PrincipalPublicKey:
        """
        Add service principal public key
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "principal": principal,
        }

        path = Template("/system/identity/v2beta1/principals/${principal}/keys").substitute(path_params)
        url = self.base_client.build_url(path)
        data = ec_jwk.to_dict()
        response = self.base_client.post(url, json=data, params=query_params)
        return handle_response(response, PrincipalPublicKey)

    def add_role_permission(self, role: str, body: str, query_params: Dict[str, object] = None) -> RolePermission:
        """
        Adds permissions to a role in a given tenant.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "role": role,
        }

        path = Template("/identity/v2beta1/roles/${role}/permissions").substitute(path_params)
        url = self.base_client.build_url(path)
        data = body
        response = self.base_client.post(url, json=data, params=query_params)
        return handle_response(response, RolePermission)

    def create_group(self, create_group_body: CreateGroupBody, query_params: Dict[str, object] = None) -> Group:
        """
        Creates a new group in a given tenant.
        """
        if query_params is None:
            query_params = {}

        path_params = {
        }

        path = Template("/identity/v2beta1/groups").substitute(path_params)
        url = self.base_client.build_url(path)
        data = create_group_body.to_dict()
        response = self.base_client.post(url, json=data, params=query_params)
        return handle_response(response, Group)

    def create_identity_provider(self, identity_provider_config_body: IdentityProviderConfigBody, query_params: Dict[str, object] = None) -> IdentityProviderBody:
        """
        Create an Identity Provider.
        """
        if query_params is None:
            query_params = {}

        path_params = {
        }

        path = Template("/identity/v2beta1/identityproviders").substitute(path_params)
        url = self.base_client.build_url(path)
        data = identity_provider_config_body.to_dict()
        response = self.base_client.post(url, json=data, params=query_params)
        return handle_response(response, IdentityProviderBody)

    def create_principal(self, create_principal_body: CreatePrincipalBody, invite_id: str = None, query_params: Dict[str, object] = None) -> Principal:
        """
        Create a new principal
        """
        if query_params is None:
            query_params = {}
        if invite_id is not None:
            query_params['inviteID'] = invite_id

        path_params = {
        }

        path = Template("/system/identity/v2beta1/principals").substitute(path_params)
        url = self.base_client.build_url(path)
        data = create_principal_body.to_dict()
        response = self.base_client.post(url, json=data, params=query_params)
        return handle_response(response, Principal)

    def create_role(self, create_role_body: CreateRoleBody, query_params: Dict[str, object] = None) -> Role:
        """
        Creates a new authorization role in a given tenant.
        """
        if query_params is None:
            query_params = {}

        path_params = {
        }

        path = Template("/identity/v2beta1/roles").substitute(path_params)
        url = self.base_client.build_url(path)
        data = create_role_body.to_dict()
        response = self.base_client.post(url, json=data, params=query_params)
        return handle_response(response, Role)

    def delete_group(self, group: str, query_params: Dict[str, object] = None) -> SSCVoidModel:
        """
        Deletes a group in a given tenant.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "group": group,
        }

        path = Template("/identity/v2beta1/groups/${group}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.delete(url, params=query_params)
        return handle_response(response, )

    def delete_identity_provider(self, idp: str, query_params: Dict[str, object] = None) -> SSCVoidModel:
        """
        Deletes the Identity Provider.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "idp": idp,
        }

        path = Template("/identity/v2beta1/identityproviders/${idp}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.delete(url, params=query_params)
        return handle_response(response, )

    def delete_principal_public_key(self, principal: str, key_id: str, query_params: Dict[str, object] = None) -> SSCVoidModel:
        """
        Deletes principal public key
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "principal": principal,
            "keyId": key_id,
        }

        path = Template("/system/identity/v2beta1/principals/${principal}/keys/${keyId}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.delete(url, params=query_params)
        return handle_response(response, )

    def delete_role(self, role: str, query_params: Dict[str, object] = None) -> SSCVoidModel:
        """
        Deletes a defined role for a given tenant.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "role": role,
        }

        path = Template("/identity/v2beta1/roles/${role}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.delete(url, params=query_params)
        return handle_response(response, )

    def get_group(self, group: str, query_params: Dict[str, object] = None) -> Group:
        """
        Returns information about a given group within a tenant.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "group": group,
        }

        path = Template("/identity/v2beta1/groups/${group}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, Group)

    def get_group_member(self, group: str, member: str, query_params: Dict[str, object] = None) -> GroupMember:
        """
        Returns information about a given member within a given group.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "group": group,
            "member": member,
        }

        path = Template("/identity/v2beta1/groups/${group}/members/${member}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, GroupMember)

    def get_group_role(self, group: str, role: str, query_params: Dict[str, object] = None) -> GroupRole:
        """
        Returns information about a given role within a given group.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "group": group,
            "role": role,
        }

        path = Template("/identity/v2beta1/groups/${group}/roles/${role}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, GroupRole)

    def get_identity_provider(self, idp: str, query_params: Dict[str, object] = None) -> IdentityProviderBody:
        """
        Returns the Identity Provider for the given tenant.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "idp": idp,
        }

        path = Template("/identity/v2beta1/identityproviders/${idp}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, IdentityProviderBody)

    def get_member(self, member: str, query_params: Dict[str, object] = None) -> Member:
        """
        Returns a member of a given tenant.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "member": member,
        }

        path = Template("/identity/v2beta1/members/${member}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, Member)

    def get_principal(self, principal: str, query_params: Dict[str, object] = None) -> Principal:
        """
        Returns the details of a principal, including its tenant membership.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "principal": principal,
        }

        path = Template("/system/identity/v2beta1/principals/${principal}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, Principal)

    def get_principal_public_key(self, principal: str, key_id: str, query_params: Dict[str, object] = None) -> PrincipalPublicKey:
        """
        Returns principal public key
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "principal": principal,
            "keyId": key_id,
        }

        path = Template("/system/identity/v2beta1/principals/${principal}/keys/${keyId}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, PrincipalPublicKey)

    def get_principal_public_keys(self, principal: str, query_params: Dict[str, object] = None) -> List[PrincipalPublicKey]:
        """
        Returns principal public keys
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "principal": principal,
        }

        path = Template("/system/identity/v2beta1/principals/${principal}/keys").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, PrincipalPublicKey)

    def get_role(self, role: str, query_params: Dict[str, object] = None) -> Role:
        """
        Returns a role for a given tenant.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "role": role,
        }

        path = Template("/identity/v2beta1/roles/${role}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, Role)

    def get_role_permission(self, role: str, permission: str, query_params: Dict[str, object] = None) -> RolePermission:
        """
        Gets a permission for the specified role.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "role": role,
            "permission": permission,
        }

        path = Template("/identity/v2beta1/roles/${role}/permissions/${permission}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, RolePermission)

    def list_group_members(self, group: str, query_params: Dict[str, object] = None) -> List[str]:
        """
        Returns a list of the members within a given group.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "group": group,
        }

        path = Template("/identity/v2beta1/groups/${group}/members").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, str)

    def list_group_roles(self, group: str, query_params: Dict[str, object] = None) -> List[str]:
        """
        Returns a list of the roles that are attached to a group within a given tenant.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "group": group,
        }

        path = Template("/identity/v2beta1/groups/${group}/roles").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, str)

    def list_groups(self, access: str = None, query_params: Dict[str, object] = None) -> List[str]:
        """
        List the groups that exist in a given tenant.
        """
        if query_params is None:
            query_params = {}
        if access is not None:
            query_params['access'] = access

        path_params = {
        }

        path = Template("/identity/v2beta1/groups").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, str)

    def list_identity_provider(self, query_params: Dict[str, object] = None) -> List[IdentityProviderBody]:
        """
        Returns the list of Identity Providers for the given tenant.
        """
        if query_params is None:
            query_params = {}

        path_params = {
        }

        path = Template("/identity/v2beta1/identityproviders").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, IdentityProviderBody)

    def list_member_groups(self, member: str, query_params: Dict[str, object] = None) -> List[str]:
        """
        Returns a list of groups that a member belongs to within a tenant.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "member": member,
        }

        path = Template("/identity/v2beta1/members/${member}/groups").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, str)

    def list_member_permissions(self, member: str, scope_filter: str = None, query_params: Dict[str, object] = None) -> List[str]:
        """
        Returns a set of permissions granted to the member within the tenant.

        """
        if query_params is None:
            query_params = {}
        if scope_filter is not None:
            query_params['scopeFilter'] = scope_filter

        path_params = {
            "member": member,
        }

        path = Template("/identity/v2beta1/members/${member}/permissions").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, str)

    def list_member_roles(self, member: str, query_params: Dict[str, object] = None) -> List[str]:
        """
        Returns a set of roles that a given member holds within the tenant.

        """
        if query_params is None:
            query_params = {}

        path_params = {
            "member": member,
        }

        path = Template("/identity/v2beta1/members/${member}/roles").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, str)

    def list_members(self, query_params: Dict[str, object] = None) -> List[str]:
        """
        Returns a list of members in a given tenant.
        """
        if query_params is None:
            query_params = {}

        path_params = {
        }

        path = Template("/identity/v2beta1/members").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, str)

    def list_principals(self, query_params: Dict[str, object] = None) -> List[str]:
        """
        Returns the list of principals that the Identity service knows about.
        """
        if query_params is None:
            query_params = {}

        path_params = {
        }

        path = Template("/system/identity/v2beta1/principals").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, str)

    def list_role_groups(self, role: str, query_params: Dict[str, object] = None) -> List[str]:
        """
        Gets a list of groups for a role in a given tenant.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "role": role,
        }

        path = Template("/identity/v2beta1/roles/${role}/groups").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, str)

    def list_role_permissions(self, role: str, query_params: Dict[str, object] = None) -> List[str]:
        """
        Gets the permissions for a role in a given tenant.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "role": role,
        }

        path = Template("/identity/v2beta1/roles/${role}/permissions").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, str)

    def list_roles(self, query_params: Dict[str, object] = None) -> List[str]:
        """
        Returns all roles for a given tenant.
        """
        if query_params is None:
            query_params = {}

        path_params = {
        }

        path = Template("/identity/v2beta1/roles").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, str)

    def remove_group_member(self, group: str, member: str, query_params: Dict[str, object] = None) -> SSCVoidModel:
        """
        Removes the member from a given group.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "group": group,
            "member": member,
        }

        path = Template("/identity/v2beta1/groups/${group}/members/${member}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.delete(url, params=query_params)
        return handle_response(response, )

    def remove_group_role(self, group: str, role: str, query_params: Dict[str, object] = None) -> SSCVoidModel:
        """
        Removes a role from a given group.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "group": group,
            "role": role,
        }

        path = Template("/identity/v2beta1/groups/${group}/roles/${role}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.delete(url, params=query_params)
        return handle_response(response, )

    def remove_member(self, member: str, query_params: Dict[str, object] = None) -> SSCVoidModel:
        """
        Removes a member from a given tenant
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "member": member,
        }

        path = Template("/identity/v2beta1/members/${member}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.delete(url, params=query_params)
        return handle_response(response, )

    def remove_role_permission(self, role: str, permission: str, query_params: Dict[str, object] = None) -> SSCVoidModel:
        """
        Removes a permission from the role.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "role": role,
            "permission": permission,
        }

        path = Template("/identity/v2beta1/roles/${role}/permissions/${permission}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.delete(url, params=query_params)
        return handle_response(response, )

    def revoke_principal_auth_tokens(self, principal: str, query_params: Dict[str, object] = None) -> SSCVoidModel:
        """
        Revoke all existing tokens issued to a principal. Principals can reset their password by visiting https://login.splunk.com/en_us/page/lost_password
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "principal": principal,
        }

        path = Template("/system/identity/v2beta1/principals/${principal}/revoke").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.post(url, params=query_params)
        return handle_response(response, )

    def update_identity_provider(self, idp: str, identity_provider_config_body: IdentityProviderConfigBody, query_params: Dict[str, object] = None) -> IdentityProviderBody:
        """
        Update the configuration for an Identity Provider.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "idp": idp,
        }

        path = Template("/identity/v2beta1/identityproviders/${idp}").substitute(path_params)
        url = self.base_client.build_url(path)
        data = identity_provider_config_body.to_dict()
        response = self.base_client.put(url, json=data, params=query_params)
        return handle_response(response, IdentityProviderBody)

    def update_principal_public_key(self, principal: str, key_id: str, principal_public_key_status_body: PrincipalPublicKeyStatusBody, query_params: Dict[str, object] = None) -> PrincipalPublicKey:
        """
        Update principal public key
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "principal": principal,
            "keyId": key_id,
        }

        path = Template("/system/identity/v2beta1/principals/${principal}/keys/${keyId}").substitute(path_params)
        url = self.base_client.build_url(path)
        data = principal_public_key_status_body.to_dict()
        response = self.base_client.put(url, json=data, params=query_params)
        return handle_response(response, PrincipalPublicKey)

    def validate_token(self, include: List[str] = None, query_params: Dict[str, object] = None) -> ValidateInfo:
        """
        Validates the access token obtained from the authorization header and returns the principal name and tenant memberships.

        """
        if query_params is None:
            query_params = {}
        if include is not None:
            query_params['include'] = include

        path_params = {
        }

        path = Template("/identity/v2beta1/validate").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, ValidateInfo)


