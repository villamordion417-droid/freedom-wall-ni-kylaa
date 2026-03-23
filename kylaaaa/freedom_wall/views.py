from django.shortcuts import render
from .models import Post

def wall(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'freedom_wall/wall.html', {'posts': posts})
