from django.contrib import admin

from .models import Document, User

admin.site.register(User)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "filetype", "downloads", "emails")
