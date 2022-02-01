import datetime

import click

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

from koapy.config import default_encoding


def generate_self_signed_key_cert(
    organization_name,
    common_name,
    key_filename=None,
    cert_filename=None,
    key_password=None,
    country_name=None,
    state_or_province_name=None,
    locality_name=None,
    valid_days=None,
):
    # generate root ca key
    root_ca_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    encryption_algorithm = serialization.NoEncryption()
    if key_password is not None:
        if not isinstance(key_password, bytes):
            encoding = default_encoding
            key_password = key_password.encode(encoding)
        encryption_algorithm = serialization.BestAvailableEncryption(key_password)
    root_ca_key_bytes = root_ca_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=encryption_algorithm,
    )
    if key_filename is None:
        key_filename = "root_ca_key.pem"
    with open(key_filename, "wb") as f:
        f.write(root_ca_key_bytes)

    # generate root ca cert
    name_attributes = []
    if country_name is not None:
        name_attributes.append(x509.NameAttribute(NameOID.COUNTRY_NAME, country_name))
    if state_or_province_name is not None:
        name_attributes.append(
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state_or_province_name)
        )
    if locality_name is not None:
        name_attributes.append(x509.NameAttribute(NameOID.LOCALITY_NAME, locality_name))
    name_attributes += [
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization_name),
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
    ]
    subject = issuer = x509.Name(name_attributes)
    cert_builder = x509.CertificateBuilder()
    cert_builder = cert_builder.subject_name(subject)
    cert_builder = cert_builder.issuer_name(issuer)
    cert_builder = cert_builder.public_key(root_ca_key.public_key())
    cert_builder = cert_builder.serial_number(x509.random_serial_number())
    if valid_days is None:
        valid_days = 356 * 10
    not_valid_before = datetime.datetime.utcnow()
    not_valid_after = not_valid_before + datetime.timedelta(days=valid_days)
    cert_builder = cert_builder.not_valid_before(not_valid_before)
    cert_builder = cert_builder.not_valid_after(not_valid_after)
    cert_builder = cert_builder.add_extension(
        x509.SubjectAlternativeName([x509.DNSName("localhost")]),
        critical=False,
    )
    root_ca_cert = cert_builder.sign(root_ca_key, hashes.SHA256())
    root_ca_cert_bytes = root_ca_cert.public_bytes(serialization.Encoding.PEM)
    if cert_filename is None:
        cert_filename = "root_ca_cert.pem"
    with open(cert_filename, "wb") as f:
        f.write(root_ca_cert_bytes)


def generate_key_cert_signed_by_authority(
    organization_name,
    common_name,
    alternative_dns_names=None,
    key_filename=None,
    csr_filename=None,
    cert_filename=None,
    key_password=None,
    country_name=None,
    state_or_province_name=None,
    locality_name=None,
    valid_days=None,
    authority_key_filename=None,
    authority_cert_filename=None,
    authority_key_password=None,
):
    # generate server key
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    encryption_algorithm = serialization.NoEncryption()
    if key_password is not None:
        if not isinstance(key_password, bytes):
            encoding = default_encoding
            key_password = key_password.encode(encoding)
        encryption_algorithm = serialization.BestAvailableEncryption(key_password)
    key_bytes = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=encryption_algorithm,
    )
    if key_filename is None:
        key_filename = "key.pem"
    with open(key_filename, "wb") as f:
        f.write(key_bytes)

    # generate server csr
    name_attributes = []
    if country_name is not None:
        name_attributes.append(x509.NameAttribute(NameOID.COUNTRY_NAME, country_name))
    if state_or_province_name is not None:
        name_attributes.append(
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state_or_province_name)
        )
    if locality_name is not None:
        name_attributes.append(x509.NameAttribute(NameOID.LOCALITY_NAME, locality_name))
    name_attributes += [
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization_name),
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
    ]
    subject = x509.Name(name_attributes)
    csr_builder = x509.CertificateSigningRequestBuilder()
    csr_builder = csr_builder.subject_name(subject)
    if alternative_dns_names is None:
        alternative_dns_names = ["localhost"]
    csr_builder = csr_builder.add_extension(
        x509.SubjectAlternativeName(
            [x509.DNSName(name) for name in alternative_dns_names]
        ),
        critical=False,
    )
    csr = csr_builder.sign(key, hashes.SHA256())
    csr_bytes = csr.public_bytes(serialization.Encoding.PEM)
    if csr_filename is None:
        csr_filename = "csr.pem"
    with open(csr_filename, "wb") as f:
        f.write(csr_bytes)

    # get authority key and cert
    if authority_key_password is not None:
        if not isinstance(authority_key_password, bytes):
            encoding = default_encoding
            authority_key_password = authority_key_password.encode(encoding)
    if authority_key_filename is None:
        authority_key_filename = "root_ca_key.pem"
    with open(authority_key_filename, "rb") as f:
        authority_key = serialization.load_pem_private_key(
            f.read(),
            password=authority_key_password,
        )
    if authority_cert_filename is None:
        authority_cert_filename = "root_ca_cert.pem"
    with open(authority_cert_filename, "rb") as f:
        authority_cert = x509.load_pem_x509_certificate(f.read())

    # root ca signs and issues server cert from server csr
    cert_builder = x509.CertificateBuilder()
    cert_builder = cert_builder.subject_name(subject)
    cert_builder = cert_builder.issuer_name(authority_cert.subject)
    cert_builder = cert_builder.public_key(csr.public_key())
    cert_builder = cert_builder.serial_number(x509.random_serial_number())
    if valid_days is None:
        valid_days = 356
    not_valid_before = datetime.datetime.utcnow()
    not_valid_after = not_valid_before + datetime.timedelta(days=valid_days)
    cert_builder = cert_builder.not_valid_before(not_valid_before)
    cert_builder = cert_builder.not_valid_after(not_valid_after)
    for extension in csr.extensions:
        cert_builder = cert_builder.add_extension(
            extension.value,
            critical=extension.critical,
        )
    cert = cert_builder.sign(authority_key, hashes.SHA256())
    cert_bytes = cert.public_bytes(serialization.Encoding.PEM)
    if cert_filename is None:
        cert_filename = "cert.pem"
    with open(cert_filename, "wb") as f:
        f.write(cert_bytes)


@click.command(
    short_help="Generate crypto-related files for server/client SSL/TLS.",
)
def ssl_credentials():
    # generate root ca key and cert
    root_ca_organization_name = "Root CA"
    root_ca_common_name = "localhost"
    root_ca_key_filename = "root_ca_key.pem"
    root_ca_cert_filename = "root_ca_cert.pem"
    generate_self_signed_key_cert(
        root_ca_organization_name,
        root_ca_common_name,
        key_filename=root_ca_key_filename,
        cert_filename=root_ca_cert_filename,
    )

    # generate server key and cert
    server_organization_name = "Server"
    server_common_name = "localhost"
    server_key_filename = "server_key.pem"
    server_csr_filename = "server_csr.pem"
    server_cert_filename = "server_cert.pem"
    generate_key_cert_signed_by_authority(
        server_organization_name,
        server_common_name,
        key_filename=server_key_filename,
        csr_filename=server_csr_filename,
        cert_filename=server_cert_filename,
        authority_key_filename=root_ca_key_filename,
        authority_cert_filename=root_ca_cert_filename,
    )

    # generate client key and cert
    client_organization_name = "Client"
    client_common_name = "localhost"
    client_key_filename = "client_key.pem"
    client_csr_filename = "client_csr.pem"
    client_cert_filename = "client_cert.pem"
    generate_key_cert_signed_by_authority(
        client_organization_name,
        client_common_name,
        key_filename=client_key_filename,
        csr_filename=client_csr_filename,
        cert_filename=client_cert_filename,
        authority_key_filename=root_ca_key_filename,
        authority_cert_filename=root_ca_cert_filename,
    )
