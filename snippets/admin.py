from django.contrib import admin

from .models import Snippet


class SnippetAdmin(admin.ModelAdmin):
    pass


admin.site.register(Snippet, SnippetAdmin)
