def main():
    import grpc

    from koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceClient import (
        KiwoomOpenApiPlusServiceClient,
    )

    host = "localhost"
    port = 8888

    with open("server.crt", "rb") as f:
        server_crt = f.read()

    credentials = grpc.ssl_channel_credentials(
        root_certificates=server_crt,
        private_key=None,
        certificate_chain=None,
    )

    client = KiwoomOpenApiPlusServiceClient(
        host=host, port=port, credentials=credentials
    )
    client.EnsureConnected()


if __name__ == "__main__":
    main()
