import base64
import json

from celery import shared_task
from django.core.files.base import ContentFile

from .models import SDXLImageArtifact
from .utils import send_generation_request_to_sdxl


@shared_task
def send_generation_request_to_sdxl_task(event):
    engine_id = event.pop("engine_id")

    # Send request
    try:
        result = send_generation_request_to_sdxl(engine_id, event)
    except Exception as e:
        raise Exception(f"Error: {e} | {e.response.text}") from None
    artifacts = result["artifacts"]

    def get_image_artifact_objects():
        for artifact in artifacts:
            ext = "png"
            finish_reason = artifact["finishReason"]
            seed = artifact["seed"]
            base64_image = artifact["base64"]
            # Convert base64 to image
            image_data = ContentFile(
                base64.b64decode(base64_image), name=f"artifact_{seed}.{ext}"
            )

            # Create and save the artifact
            yield SDXLImageArtifact(
                image=image_data,
                finish_reason=finish_reason,
                seed=seed,
                payload=json.dumps(event),
            )

    generated_artifacts = SDXLImageArtifact.objects.bulk_create(
        get_image_artifact_objects()
    )
    return [
        {
            "id": gen_artifact.id,
            "seed": gen_artifact.seed,
            "finishReason": gen_artifact.finish_reason,
            "image": gen_artifact.image.url,
        }
        for gen_artifact in generated_artifacts
    ]
