from rest_framework import serializers


class TextPromptSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=1000)
    weight = serializers.FloatField(min_value=0.0, max_value=1.0, required=False)

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Text cannot be empty.")
        return value


class SDXLImageGenerationSerializer(serializers.Serializer):
    engine_id = serializers.ChoiceField(
        choices=[
            "stable-diffusion-xl-1024-v1-0",
            "stable-diffusion-v1-6",
            "stable-diffusion-xl-beta-v2-2-2",
        ],
        default="stable-diffusion-xl-1024-v1-0",
    )

    text_prompts = serializers.ListField(
        child=TextPromptSerializer(), min_length=1, required=True
    )
    height = serializers.IntegerField(default=512, min_value=128)
    width = serializers.IntegerField(default=512, min_value=128)
    cfg_scale = serializers.FloatField(min_value=0, max_value=35, default=7)
    clip_guidance_preset = serializers.ChoiceField(
        choices=[
            "FAST_BLUE",
            "FAST_GREEN",
            "NONE",
            "SIMPLE",
            "SLOW",
            "SLOWER",
            "SLOWEST",
        ],
        default="NONE",
    )
    sampler = serializers.ChoiceField(
        choices=[
            "DDIM",
            "DDPM",
            "K_DPMPP_2M",
            "K_DPMPP_2S_ANCESTRAL",
            "K_DPM_2",
            "K_DPM_2_ANCESTRAL",
            "K_EULER",
            "K_EULER_ANCESTRAL",
            "K_HEUN",
            "K_LMS",
        ],
        default="DDIM",
    )
    samples = serializers.IntegerField(min_value=1, max_value=10, default=1)
    seed = serializers.IntegerField(min_value=0, max_value=4294967295, default=0)
    steps = serializers.IntegerField(min_value=10, max_value=50, default=30)
    style_preset = serializers.ChoiceField(
        choices=[
            "3d-model",
            "analog-film",
            "anime",
            "cinematic",
            "comic-book",
            "digital-art",
            "enhance",
            "fantasy-art",
            "isometric",
            "line-art",
            "low-poly",
            "modeling-compound",
            "neon-punk",
            "origami",
            "photographic",
            "pixel-art",
            "tile-texture",
        ],
        required=False,
    )
    extras = serializers.JSONField(required=False)

    def validate_height(self, value):
        if value % 64 != 0:
            raise serializers.ValidationError("Height must be a multiple of 64.")
        return value

    def validate_width(self, value):
        if value % 64 != 0:
            raise serializers.ValidationError("Width must be a multiple of 64.")
        return value


class ImageSerializer(serializers.Serializer):
    base64 = serializers.CharField()  # Represents a base64-encoded image string


class SDXLResponseSerializer(serializers.Serializer):
    artifacts = ImageSerializer(many=True)
    finishReason = serializers.ChoiceField(
        choices=["CONTENT_FILTERED", "ERROR", "SUCCESS"]
    )
    seed = serializers.IntegerField()
