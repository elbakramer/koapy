def generate_tls_certificate(ou, cn):
    import random

    import OpenSSL

    cert_seconds_to_expiry = 60 * 60 * 24 * 365  # one year

    key = OpenSSL.crypto.PKey()
    key.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)

    cert = OpenSSL.crypto.X509()
    cert.get_subject().OU = ou
    cert.get_subject().CN = cn
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(cert_seconds_to_expiry)
    cert.set_serial_number(random.getrandbits(64))
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(key)
    cert.sign(key, "sha256")

    with open("server.key", "wb") as f:
        f.write(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, key))
    with open("server.crt", "wb") as f:
        f.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert))


def main():
    import signal
    import sys

    import grpc

    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidget import (
        KiwoomOpenApiPlusQAxWidget,
    )
    from koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceServer import (
        KiwoomOpenApiPlusServiceServer,
    )
    from koapy.compat.pyside2.QtWidgets import QApplication

    host = "0.0.0.0"
    port = 8888

    app = QApplication.instance()

    if not app:
        app = QApplication(sys.argv)

    control = KiwoomOpenApiPlusQAxWidget()

    with open("server.key", "rb") as f:
        server_key = f.read()
    with open("server.crt", "rb") as f:
        server_crt = f.read()

    credentials = grpc.ssl_server_credentials(
        private_key_certificate_chain_pairs=((server_key, server_crt),),
        root_certificates=None,
        require_client_auth=False,
    )

    server = KiwoomOpenApiPlusServiceServer(
        control, host=host, port=port, credentials=credentials
    )

    # for Ctrl+C to work
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    server.start()
    app.exec_()


if __name__ == "__main__":
    main()
