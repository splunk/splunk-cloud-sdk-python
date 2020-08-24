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
import pytest
import time

from splunk_sdk.base_client import BaseClient
from splunk_sdk.catalog import MetadataCatalog
from splunk_sdk.catalog import IndexDatasetPOST, IndexDatasetKind, \
    ImportDatasetPOST, ImportDatasetByIdPOST, RulePOST, LookupDatasetPOST, \
    LookupDatasetExternalKind, FieldPOST, FieldPrevalence, FieldType, \
    FieldDataType, FieldPATCH
from test.fixtures import get_test_client as test_client  # NOQA


def _randint() -> int:
    return random.randint(0, 100000000)


def _create_ds_name(name: str) -> str:
    return "pyintegds{}_{}".format(name, _randint())


@pytest.mark.usefixtures("test_client")  # NOQA
def test_create_delete_index_and_import(test_client: BaseClient):
    catalog = MetadataCatalog(test_client)
    name = _create_ds_name("py_cr_idx")
    idx = catalog.create_dataset(IndexDatasetPOST(name=name, disabled=False))
    assert (name == idx.name)

    import_name = _create_ds_name("py_cr_imp")
    time.sleep(2)
    imp = catalog.create_dataset(ImportDatasetByIdPOST(name=import_name, source_id=idx.id))
    assert (imp.name == import_name)
    catalog.delete_dataset(import_name)
    catalog.delete_dataset(name)


@pytest.mark.usefixtures("test_client")  # NOQA
def test_retrieve_datasets(test_client: BaseClient):
    catalog = MetadataCatalog(test_client)
    datasets = catalog.list_datasets()
    assert (len(datasets) > 0)


@pytest.mark.usefixtures("test_client")  # NOQA
def test_retreive_datasets_with_filter(test_client: BaseClient):
    catalog = MetadataCatalog(test_client)
    datasets = catalog.list_datasets(filter='version==2')
    assert (len(datasets) > 0)

@pytest.mark.usefixtures("test_client")  # NOQA
def test_create_list_delete_rule(test_client: BaseClient):
    catalog = MetadataCatalog(test_client)
    rule_name = _create_ds_name("py_cr_rule")
    rule = catalog.create_rule(RulePOST(name=rule_name, match="sourcetype::integration_test_match"))
    assert (rule.name == rule_name)
    rules = catalog.list_rules()
    assert (len(rules) >= 1)
    rules = catalog.list_rules(filter='name=="' + rule_name + '"')
    assert (len(rules) == 1)
    catalog.delete_rule(rule_name)
    rules = catalog.list_rules(filter='name=="' + rule_name + '"')
    assert (len(rules) == 0)


@pytest.mark.usefixtures("test_client")  # NOQA
def test_dataset_fields(test_client: BaseClient):
    catalog = MetadataCatalog(test_client)
    int_test_field_1 = "integ_test_field1"
    int_test_field_2 = "integ_test_field2"
    lookup_name = _create_ds_name("py_cr_lookup")
    lookup = catalog.create_dataset(
        LookupDatasetPOST(name=lookup_name, external_kind=LookupDatasetExternalKind.KVCOLLECTION,
                          external_name="test_external_name"))
    time.sleep(1)
    field1 = catalog.create_field_for_dataset_by_id(lookup.id,
                                                    FieldPOST(name=int_test_field_1, datatype=FieldDataType.STRING,
                                                              fieldtype=FieldType.DIMENSION,
                                                              prevalence=FieldPrevalence.ALL))
    time.sleep(1)
    ret_field1 = catalog.get_field_by_id_for_dataset_by_id(datasetid=lookup.id, fieldid=field1.id)
    assert(field1.name == ret_field1.name)
    fields = catalog.list_fields_for_dataset_by_id(lookup.id)
    assert(len(fields) == 1)
    catalog.update_field_by_id_for_dataset_by_id(lookup.id, field1.id, FieldPATCH(name=int_test_field_2))
    time.sleep(1)
    ret_field1 = catalog.get_field_by_id_for_dataset_by_id(datasetid=lookup.id, fieldid=field1.id)
    assert(ret_field1.name == int_test_field_2)
    catalog.delete_field_by_id_for_dataset_by_id(lookup.id, field1.id)
    catalog.delete_dataset_by_id(lookup.id)
