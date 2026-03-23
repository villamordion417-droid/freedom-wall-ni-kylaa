from django.db import models

class Post(models.Model):
    EMOTION_CHOICES = [
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('angry', 'Angry'),
        ('excited', 'Excited'),
        ('anxious', 'Anxious'),
        ('neutral', 'Neutral'),
    ]
    content = models.TextField()
    emotion = models.CharField(max_length=10, choices=EMOTION_CHOICES, default='neutral')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.emotion}: {self.content[:50]}"
