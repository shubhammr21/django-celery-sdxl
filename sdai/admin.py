from django.contrib import admin
from django.utils.html import format_html

from .models import SDXLImageArtifact


@admin.register(SDXLImageArtifact)
class SDXLImageArtifactAdmin(admin.ModelAdmin):
    list_display = ["get_image", "finish_reason", "seed", "created_at", "updated_at"]
    search_fields = [
        "finish_reason",
        "seed",
    ]  # Removed 'image' as it is a FileField and cannot be searched directly.
    list_filter = [
        "finish_reason",
        "seed",
        "created_at",
    ]  # Added 'created_at' to filter by date.
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        (
            "Artifact Details",
            {"fields": ("image", "finish_reason", "seed", "created_at", "updated_at")},
        ),
    )
    ordering = ["-created_at"]
    list_per_page = 10
    list_max_show_all = 100
    list_display_links = [
        "finish_reason",
        "seed",
    ]  # Changed from 'image' as it will be a clickable link.

    # Display image in list view as a link to the image file
    def get_image(self, obj):
        if obj.image:
            return format_html(
                '<a href="{0}" target="_blank"><img src="{0}" width="150" style="width: auto; height: auto; max-width: 100px; max-height: 100px; object-fit: scale-down;" />{1}</a>',
                obj.image.url,
                obj.image.name,
            )

        return "-"

    get_image.short_description = (
        "Image"  # Sets the column header for this custom field
    )
