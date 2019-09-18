# Copyright © 2019 Splunk, Inc.
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import pytest
import time
from test.fixtures import get_test_client as test_client  # NOQA
from splunk_sdk.catalog import MetadataCatalog as Catalog, \
    KVCollectionDatasetPOST, Dataset
from splunk_sdk.kvstore import KVStoreAPI, IndexDefinition, \
    IndexFieldDefinition
from splunk_sdk.common.sscmodel import SSCModel


class Record(SSCModel):

    def __init__(self):
        super().__init__()

    def to_dict(self) -> dict:
        return self.__dict__


def _create_dataset(test_client) -> Dataset:
    catalog = Catalog(test_client)
    name = "pysdk" + str(time.time_ns())
    result = catalog.create_dataset(KVCollectionDatasetPOST(name))
    assert (result is not None)
    return result


def _delete_dataset(test_client, name):
    catalog = Catalog(test_client)
    resp = catalog.delete_dataset(name).response
    assert(resp.status_code == 204)


@pytest.mark.usefixtures('test_client')  # NOQA
def test_ping(test_client):
    kvs = KVStoreAPI(test_client)
    health = kvs.ping()
    assert(health.status == 'healthy')


@pytest.mark.usefixtures('test_client')  # NOQA
def test_create_and_delete_dataset(test_client):
    ds = _create_dataset(test_client)
    _delete_dataset(test_client, ds.name)


@pytest.mark.usefixtures('test_client')  # NOQA
def test_index_operations(test_client):

    # create kvcollection dataset
    ds = _create_dataset(test_client)
    collection_name = ds.name
    index_name = "myindex"

    kvs = KVStoreAPI(test_client)
    fields = [IndexFieldDefinition(direction=1, field="f1"), ]

    # create index
    index_description = kvs.create_index(collection=collection_name,
                                         index_definition=IndexDefinition(
                                             fields=fields, name=index_name))
    assert(index_description.name == index_name)
    assert(index_description.fields[0].direction == fields[0].direction)
    assert(index_description.fields[0].field == fields[0].field)

    # list indexes
    indexes = kvs.list_indexes(collection_name)
    assert(indexes[0].fields[0].direction == fields[0].direction)
    assert(indexes[0].fields[0].field == fields[0].field)

    # Note: delete_index returns 404
    # delete index and collection
    # kvs.delete_index(collection=collection_name, index=index_name)
    _delete_dataset(test_client, collection_name)


@pytest.mark.usefixtures('test_client')  # NOQA
def test_record_operations(test_client):

    # create kvcollection dataset
    ds = _create_dataset(test_client)
    collection_name = ds.name
    index_name = "myindex"
    my_data = "mydata"

    kvs = KVStoreAPI(test_client)
    fields = [IndexFieldDefinition(direction=1, field="f1"), ]

    # create index
    index_description = kvs.create_index(collection=collection_name,
                                         index_definition=IndexDefinition(
                                             fields=fields, name=index_name))
    assert(index_description.name == index_name)

    r1 = Record()
    r1.column = my_data

    r2 = Record()
    r2.data = "backups"

    r3 = Record()
    r3.level = "logs"

    # insert a record
    key = kvs.insert_record(collection_name, body=r1)
    assert(key is not None)
    assert(key.key is not None)

    # insert two records
    keys = kvs.insert_records(collection_name, request_body=[r2, r3])
    assert(keys is not None)
    assert(len(keys) == 2)

    # list a record
    records = kvs.list_records(collection_name, fields=['column'], count=1)
    assert(records is not None)
    assert(records[0] == {'column': my_data})

    # get record by key
    rec = kvs.get_record_by_key(collection_name, key.key)
    assert(rec is not None)
    assert(rec["_key"] == key.key)
    assert(rec["column"] == my_data)

    # put record
    r1.meta = '{"more_info": {"color": "red", "num": 23}"}'
    key = kvs.put_record(collection_name, key=key.key, body=r1)
    assert(key is not None)
    assert(key.key is not None)

    # query record
    records = kvs.query_records(collection_name, query='{"column": "mydata"}')
    assert(records is not None)
    assert(records[0]['_key'] == key.key)
    assert(records[0]['column'] == my_data)
    assert(records[0]['meta'] == '{"more_info": {"color": "red", "num": 23}"}')

    # delete record by key
    resp = kvs.delete_record_by_key(collection_name, key=key.key).response
    assert(resp.status_code == 204)

    # delete records
    resp = kvs.delete_records(collection_name).response
    assert(resp.status_code == 204)

    # Note: delete index and dataset
    # delete_index returns 404
    # kvs.delete_index(collection=collection_name, index=index_name)
    _delete_dataset(test_client, ds.name)
