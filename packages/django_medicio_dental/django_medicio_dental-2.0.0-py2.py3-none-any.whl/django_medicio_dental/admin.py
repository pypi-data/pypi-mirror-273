from django.contrib import admin
from django.db import models

from .models import Post
from mdeditor.widgets import MDEditorWidget


class PostModelAdmin (admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}
    formfield_overrides = {
        models.TextField: {'widget': MDEditorWidget}
    }


admin.site.register(Post, PostModelAdmin)