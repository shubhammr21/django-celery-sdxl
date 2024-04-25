import requests
from django.conf import settings


def send_generation_request_to_sd3(
    host,
    params,
):
    headers = {
        "Accept": "image/*",
        "Authorization": f"Bearer {settings.STABILITY_KEY}",
    }

    # Encode parameters
    files = {}
    image = params.pop("image", None)
    mask = params.pop("mask", None)
    if image is not None and image != "":
        files["image"] = open(image, "rb")
    if mask is not None and mask != "":
        files["mask"] = open(mask, "rb")
    if len(files) == 0:
        files["none"] = ""

    # Send request
    print(f"Sending REST request to {host}...")
    response = requests.post(
        host,
        headers=headers,
        files=files,
        data=params,
        timeout=60,
    )
    response.raise_for_status()

    return response


def send_generation_request_to_sdxl(
    engine_id,
    params,
):
    api_host = settings.STABILITY_API_HOST
    host = f"{api_host}/v1/generation/{engine_id}/text-to-image"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {settings.STABILITY_KEY}",
    }

    # Send request
    print(f"Sending REST request to {host}...")
    response = requests.post(
        host,
        headers=headers,
        json=params,
        timeout=60,
    )
    response.raise_for_status()

    return response.json()
