# Copyright © 2019 Splunk, Inc.
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import datetime
import pytest

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509 import NameOID

from splunk_sdk.base_client import BaseClient
from splunk_sdk.forwarders import SplunkForwarderService, Certificate
from test.fixtures import get_test_client as test_client  # NOQA


@pytest.mark.usefixtures("test_client")  # NOQA
def test_cert_crud(test_client: BaseClient):
    forwarders = SplunkForwarderService(test_client)
    forwarders.delete_certificates()

    certs = forwarders.list_certificates()
    current_cert_count = len(certs)

    cert = _generateCertificate("forwarder_01")
    cert_bytes = cert.public_bytes(serialization.Encoding.PEM).decode('utf-8')
    # FIXME: spec says that cert is a string, needs to be passed {'pem': cert}
    forwarders.add_certificate(Certificate(pem=cert_bytes))

    certs = forwarders.list_certificates()
    assert(len(certs) == current_cert_count + 1)

    forwarders.delete_certificates()
    certs = forwarders.list_certificates()
    assert(len(certs) == 0)


@pytest.mark.usefixtures("test_client")  # NOQA
def test_list_certificates(test_client: BaseClient):
    forwarders = SplunkForwarderService(test_client)
    forwarders.delete_certificates()
    _generateCertificate("bob")
    certs = forwarders.list_certificates()
    assert(len(certs) == 0)


def _generateCertificate(forwarder_name: str):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Splunk"),
        x509.NameAttribute(NameOID.COMMON_NAME, forwarder_name),
    ])

    builder = x509.CertificateBuilder()
    builder = builder.subject_name(subject)
    builder = builder.issuer_name(issuer)
    builder = builder.not_valid_before(datetime.datetime.today() - datetime.timedelta(days=1))
    builder = builder.not_valid_after(datetime.datetime.today() + datetime.timedelta(days=1))

    builder = builder.serial_number(x509.random_serial_number())
    builder = builder.public_key(private_key.public_key())
    builder = builder.add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)

    cert = builder.sign(private_key=private_key, algorithm=hashes.SHA256(), backend=default_backend())
    return cert
