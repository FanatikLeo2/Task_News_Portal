from datetime import datetime
from django.views.generic import ListView, DetailView
from .models import Post, Comment


class PostList(ListView):
    model = Post
    ordering = '-post_time_in'
    template_name = 'posts.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class CommentList(ListView):
    model = Comment
    ordering = 'comment_post'
    template_name = 'comments.html'
    context_object_name = 'comment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now()
        return context

