# Copyright © 2019 Splunk, Inc.
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import random
from time import sleep

import pytest

from splunk_sdk.base_client import BaseClient
from splunk_sdk.identity import Identity as IdentityAndAccessControl
from splunk_sdk.identity import CreateRoleBody, AddGroupRoleBody, AddMemberBody, AddGroupMemberBody, AddRolePermissionBody
from splunk_sdk.identity import CreateGroupBody
from test.fixtures import get_test_client as test_client  # NOQA


@pytest.mark.usefixtures("test_client")  # NOQA
def test_crud_groups(test_client: BaseClient):
    identity = IdentityAndAccessControl(test_client)
    username = _get_test_username(identity)

    group_name = "pygrouptest{}".format(random.randint(0, 100000000))
    group = identity.create_group(CreateGroupBody(group_name))
    assert(group.name == group_name)
    assert(test_client.get_tenant() == group.tenant)
    assert(username == group.created_by)

    sleep(2)
    fetched_group = identity.get_group(group_name)
    assert(fetched_group.created_at == group.created_at)

    all_groups = identity.list_groups()
    assert(str(all_groups.items).index(fetched_group.name) >= 0)

    role_name = "pygrouptestrole{}".format(random.randint(0, 100000000))
    role = identity.create_role(CreateRoleBody(role_name))
    assert(role.name == role_name)
    assert(role.created_by == username)

    sleep(2)
    group_role = identity.add_group_role(group_name, AddGroupRoleBody(role_name))
    assert(group_role.added_by == username)
    assert(group_role.group == group_name)
    assert(group_role.role == role_name)

    sleep(2)
    group_roles = identity.list_group_roles(group_name)
    assert(group_roles.items[0].role == role_name)

    member_name = "test1@splunk.com"
    member = identity.add_member(AddMemberBody(member_name))
    assert(member.name == member_name)
    assert(member.added_by == username)

    sleep(2)
    members = identity.list_group_members(group_name)
    members_found = [m for m in members.items if m == member_name]
    assert(len(members_found) == 0)

    group_member = identity.add_group_member(group_name, AddGroupMemberBody(name=member_name))
    assert(group_member.principal == member_name)

    sleep(2)
    members = identity.list_group_members(group_name)
    assert(str(members.items).index(member_name) >= -1)

    result_member = identity.get_group_member(group_name, member_name)
    assert(result_member.group == group_name)
    assert(result_member.principal == member_name)

    identity.remove_group_member(group_name, member_name)
    identity.remove_member(member_name)
    identity.remove_group_role(group_name, role_name)
    identity.delete_role(role_name)
    identity.delete_group(group_name)

@pytest.mark.usefixtures("test_client")  # NOQA
def test_crud_roles(test_client: BaseClient):
    test_client.context.debug = True
    identity = IdentityAndAccessControl(test_client)
    username = _get_test_username(identity)

    role_name = "pyroletest{}".format(random.randint(0, 100000000))
    role = identity.create_role(CreateRoleBody(role_name))
    assert(role.name == role_name)
    assert(role.created_by == username)
    assert(role.tenant == test_client.get_tenant())

    sleep(2)  # Role may not be ready immediately
    result_role = identity.get_role(role_name)
    assert(result_role.name == role_name)
    assert(result_role.created_by == username)
    assert(result_role.tenant == test_client.get_tenant())

    all_roles = identity.list_roles()
    assert(str(all_roles.items).index(result_role.name) >= 0)

    permission = "{}:*:pyperm1.{}".format(test_client.get_tenant(), random.randint(0, 100000000))
    result_role_perm = identity.add_role_permission(role_name, AddRolePermissionBody(permission=permission))
    assert(result_role_perm.role == role_name)
    assert(result_role_perm.permission == permission)
    assert(result_role_perm.added_by == username)
    assert(result_role_perm.tenant == test_client.get_tenant())

    sleep(2)
    retrieved_perm = identity.get_role_permission(role_name, permission)
    assert(retrieved_perm.permission == permission)

    perms = identity.list_role_permissions(role_name)
    assert(str(perms.items).index(permission) >= 0)

    identity.delete_role(role_name)


def _get_test_username(identity: IdentityAndAccessControl):
    return identity.validate_token().name
