from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'mood', 'song_title')
    list_filter = ('mood', 'created_at')
    search_fields = ('text', 'song_title', 'song_artist')