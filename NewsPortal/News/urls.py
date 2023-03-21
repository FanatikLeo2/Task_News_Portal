from django.urls import path
from .views import CommentList
from .views import PostList, PostDetail


urlpatterns = [
   path('comments/', CommentList.as_view()),
   path('news/', PostList.as_view()),
   path('news/<int:pk>', PostDetail.as_view()),
]