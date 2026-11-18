from django.contrib import admin
from .models import Investigation, FixAttempt


@admin.register(Investigation)
class InvestigationAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "priority",
        "status",
        "created_by",
        "created_at",
    )

    list_filter = ("priority", "status")
    search_fields = ("title", "description")

@admin.register(FixAttempt)
class FixAttemptAdmin(admin.ModelAdmin):
    list_display = ("investigation", "result", "created_at")
    list_filter = ("result",)
    search_fields = ("description", "solution")