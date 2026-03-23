from django.db import models


class Post(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    emotion = models.CharField(max_length=50, blank=True)
    bg_color = models.CharField(max_length=7, blank=True)
    # legacy fields kept for compatibility (not used by new flow)
    mood = models.CharField(max_length=50, blank=True)
    sentiment = models.FloatField(null=True, blank=True)
    song_title = models.CharField(max_length=200, blank=True)
    song_artist = models.CharField(max_length=200, blank=True)
    song_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.emotion} — {self.text[:30]}"