from django.urls import path
from .views import *


urlpatterns = [
   path('', PostList.as_view(), name='post_list'),
   path('search/', PostListSearch.as_view(), name='post_search'),
   path('create/', PostCreate.as_view(), name='create_post'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', ProductDelete.as_view(), name='post_delete'),
   path('comments/', CommentList.as_view()),
   path('comments/create', create_comment, name='create_comment'),
   path('comments/<str:comment_text>', show_comment, name='show_comment'),
   path('index/', index),
]
