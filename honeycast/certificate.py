# mostly taken from https://cryptography.io/en/latest/x509/reference/#x-509-certificate-builder
from .log import logger
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
import datetime

one_day = datetime.timedelta(1, 0, 0)

class Key:
    def __init__(self):
        logger.info("generating rsa key pair")
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
            backend=default_backend(),
        )

        self.public_key = self.private_key.public_key()

    def save(self, filename):
        pem_bytes = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        with open(filename, "wb") as file_handle:
            file_handle.write(pem_bytes)

class Certificate:
    def __init__(self, subject="", dns_name="", issuer="", valid_days=3650):
        logger.info("generating x509 certificate")
        self._builder = x509.CertificateBuilder()
        self._builder = self._builder.subject_name(
            x509.Name([
                x509.NameAttribute(NameOID.COMMON_NAME, subject),
            ]),
        )

        self._builder = self._builder.issuer_name(
            x509.Name([
                x509.NameAttribute(NameOID.COMMON_NAME, issuer),
            ])
        )

        today = datetime.datetime.today()
        self._builder = self._builder.not_valid_before(today - one_day)
        self._builder = self._builder.not_valid_after(today + (one_day * valid_days))

        self._builder = self._builder.serial_number(x509.random_serial_number())

        self._builder = self._builder.add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName(dns_name),
            ]),
            critical=False,
        )

        self._builder = self._builder.add_extension(
            x509.BasicConstraints(ca=False, path_length=None),
            critical=True,
        )

    def sign(self, key):
        logger.debug("signing x509 certificate with rsa key")
        builder = self._builder.public_key(key.public_key)
        certificate = builder.sign(
            private_key=key.private_key,
            algorithm=hashes.SHA256(),
            backend=default_backend(),
        )

        return SignedCertificate(certificate)

class SignedCertificate:
    def __init__(self, csr):
        self._csr = csr

    def save(self, filename):
        csr_bytes = self._csr.public_bytes(serialization.Encoding.PEM)

        with open(filename, "wb") as file_handle:
            file_handle.write(csr_bytes)
