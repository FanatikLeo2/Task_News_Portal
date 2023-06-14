from django.urls import path
from .views import *
from django.urls import path, include
from django.views.decorators.http import require_POST
from django.views.decorators.cache import cache_page


urlpatterns = [
   path('i18n/', include('django.conf.urls.i18n')), # подключаем встроенные эндопинты для работы с локализацией
   path('', PostList.as_view(), name='post_list'),
   path('search/', PostListSearch.as_view(), name='post_search'),
   path('create/', PostCreate.as_view(), name='create_post'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('comments/', CommentList.as_view()),
   path('<int:pk>/create_comment', CommentCreate.as_view(), name='comment_create'),
   path('comments/<str:comment_text>', show_comment, name='show_comment'),
   path('index/', index),
   # path('subscriptions/', subscriptions, name='subscriptions'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
   path('categories/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe'),

]
