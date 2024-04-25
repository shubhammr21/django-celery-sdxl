from django.db import models


class SDXLImageArtifact(models.Model):
    image = models.ImageField(upload_to="artifacts/")
    finish_reason = models.CharField(max_length=100)
    seed = models.IntegerField()
    payload = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Artifact {self.pk} - {self.finish_reason}"
