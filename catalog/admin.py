from django.contrib import admin

from .models import Sample


admin.site.site_header = "Administração LTPOA"
admin.site.site_title = "Administração LTPOA"
admin.site.index_title = "Gestão do laboratório"
admin.site.site_url = "/"


@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    list_display = ("code", "sample_type", "received_at", "origin", "status", "created_by")
    list_filter = ("sample_type", "status", "condition", "received_at")
    search_fields = ("code", "origin", "requester")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "received_at"
