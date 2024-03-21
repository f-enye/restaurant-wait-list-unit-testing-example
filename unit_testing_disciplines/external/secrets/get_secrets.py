import google_crc32c
from google.cloud import secretmanager


class SecretDataCorruptionError(Exception):
    pass


def get_secrets(key: str) -> str:
    """This function only serves to show how a dependency exists to obtain a value that is in a secret store (e.g. Google Secret Manager).

    This example project is not actually hosted or dependent on any GCP products.
    """

    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/some-example-project-id/secrets/{key}/versions/latest"

    response = client.access_secret_version(request={"name": name})

    _raise_for_invalid_payload_checksum(response)

    return response.payload.data.decode("UTF-8")


def _raise_for_invalid_payload_checksum(response):
    crc32c = google_crc32c.Checksum()
    crc32c.update(response.payload.data)
    if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
        raise SecretDataCorruptionError("Data corruption detected")
