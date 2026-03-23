from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('emotion', 'created_at', 'content')
    list_filter = ('emotion', 'created_at')
    search_fields = ('content',)
