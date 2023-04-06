from django.urls import reverse_lazy
from datetime import datetime
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from .models import *
from .filters import PostFilter
from .forms import PostCreateForm, CommentCreateForm


class PostList(ListView):
    model = Post
    ordering = '-post_time_in'
    template_name = 'posts.html'
    context_object_name = 'post'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now()
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class PostListSearch(ListView):
    model = Post
    ordering = '-post_time_in'
    template_name = 'search.html'
    context_object_name = 'post'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostCreateForm
    model = Post
    template_name = 'post_createform.html'

    def form_valid(self, form):
        form.instance.post_author = self.request.user.author
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('News.change_post',)
    form_class = PostCreateForm
    model = Post
    template_name = 'post_createform.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('News.delete_post',)
    model = Post
    template_name = 'post_deleteform.html'
    success_url = reverse_lazy('post_list')


class CommentList(ListView):
    # model = Comment
    queryset = Comment.objects.all()
    ordering = 'comment_post'
    template_name = 'comments.html'
    context_object_name = 'comment'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now()
        return context


def show_comment(requests, comment_text):
    com = Comment.objects.get(comment_text__iexact=comment_text)
    return render(requests, 'comment.html', context={'com': com})


class CommentCreate(LoginRequiredMixin, CreateView):
    form_class = CommentCreateForm
    model = Comment
    template_name = 'comment_createform.html'

    def form_valid(self, form):
        form.instance.comment_user = self.request.user
        form.instance.comment_post = Post.objects.get(pk=int(self.kwargs['pk']))
        return super().form_valid(form)

# def create_comment(request):
#     form = CommentCreateForm(request.POST)
#     if request.method == 'POST':
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/news/comments/')
#
#     return render(request, 'comment_createform.html', {'form': form})


def index(requests):
    posts = Post.objects.all()
    comments = Comment.objects.all()
    authors = Author.objects.all()
    categories = Category.objects.all()

    return render(requests, 'index.html',
                  context={'posts': posts, 'comments': comments, 'authors': authors, 'categories': categories})




