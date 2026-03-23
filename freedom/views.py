from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import VentForm
from .models import Post
from .utils import emotion_to_color


def index(request):
    form = VentForm(request.POST or None)
    bg_color = None
    submitted_emotion = None

    if request.method == 'POST' and form.is_valid():
        text = form.cleaned_data['text']
        emotion_input = form.cleaned_data['emotion']
        emotion, color = emotion_to_color(emotion_input)
        post = Post.objects.create(
            text=text,
            emotion=emotion,
            bg_color=color,
            created_at=timezone.now(),
        )
        bg_color = color
        submitted_emotion = emotion
        form = VentForm()  # reset

    posts = Post.objects.order_by('-created_at')[:50]
    return render(request, 'freedom/index.html', {
        'form': form,
        'posts': posts,
        'bg_color': bg_color,
        'submitted_emotion': submitted_emotion,
    })