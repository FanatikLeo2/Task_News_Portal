from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.db.models import Exists, OuterRef
from django.urls import reverse_lazy
from datetime import datetime
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from .models import *
from .filters import PostFilter
from .forms import PostCreateForm, CommentCreateForm
from django.shortcuts import redirect
import pytz
from django.core.cache import cache


class PostList(ListView):
    model = Post
    ordering = '-post_time_in'
    template_name = 'posts.html'
    context_object_name = 'post'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = timezone.now()
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/news')


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
        context['time_now'] = datetime.now()
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    # def get_object(self, *args, **kwargs):                    разобраться с кешированием
    #     obj = cache.get(f'post-{self.kwargs["pk"]}', None)
    #     if not obj:
    #         obj = super().get_object(queryset=self.queryset)
    #         cache.set(f'post-{self.kwargs["pk"]}', obj)
    #     return obj


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostCreateForm
    model = Post
    template_name = 'post_createform.html'

    def form_valid(self, form):
        form.instance.post_author = self.request.user.author
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now()
        return context


class PostUpdate(LoginRequiredMixin, UpdateView):
    # permission_required = ('News.change_post',)
    form_class = PostCreateForm
    model = Post
    template_name = 'post_createform.html'

    def form_valid(self, form):
        form.instance.post_author = self.request.user.author
        return super().form_valid(form)


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


# @login_required
# @csrf_protect
# def subscriptions(request):
#     if request.method == 'POST':
#         category_id = request.POST.get('category_id')
#         category = Category.objects.get(id=category_id)
#         action = request.POST.get('action')
#
#         if action == 'subscribe':
#             Subscription.objects.create(user=request.user, category=category)
#         elif action == 'unsubscribe':
#             Subscription.objects.filter(user=request.user, category=category).delete()
#
#     categories_with_subscriptions = Category.objects.annotate(user_subscribed=Exists(
#         Subscription.objects.filter(user=request.user, category=OuterRef('pk')))).order_by('category_name')
#
#     return render(request, 'subscriptions.html', {'categories': categories_with_subscriptions})


class CategoryListView(ListView):
    model = Post
    ordering = '-post_time_in'
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'
    paginate_by = 2


    def get_queryset(self):
        self.post_category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(post_category=self.post_category).order_by('-post_time_in')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.post_category.subscribers.all()
        context['category'] = self.post_category
        context['time_now'] = datetime.now()
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = gettext('You have successfully subscribed to the category news subscription')
    return render(request, 'subscribe.html', {'category': category, 'message': message})

@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)

    message = gettext('You have successfully unsubscribed to the category news subscription')
    return render(request, 'unsubscribe.html', {'category': category, 'message': message})