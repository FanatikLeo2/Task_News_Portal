from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import datetime


class Author(models.Model):
    author_rating = models.FloatField(default=0)
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author_user.username}'

    def update_rating(self):
        summ_rating = 0
        summ_rating += self.post_set.aggregate(postRating=Sum('post_rating'))['postRating'] * 3
        summ_rating += self.author_user.comment_set.aggregate(commentRating=Sum('comment_rating'))['commentRating']
        summ_rating += Comment.objects.filter(comment_post__in=self.post_set.all()).exclude(comment_user__author__in=[self]).aggregate(postRating=Sum('comment_rating'))['postRating']
        self.author_rating = summ_rating
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return f'{self.category_name}'


class Post(models.Model):
    NEWS = 'NE'
    ARTICLE = 'AR'
    POSTTYPES = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    ]

    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POSTTYPES, default=NEWS)
    post_time_in = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    post_title = models.CharField(max_length=255)
    post_text = models.TextField()
    post_rating = models.FloatField(default=0)

    def __str__(self):
        return f'{self.post_title}: {self.preview()}'

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return f'{self.post_text[0:123]} ...'


class PostCategory(models.Model):
    post_through = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_through = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_time_in = models.DateTimeField(auto_now_add=True)
    comment_rating = models.FloatField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()

    def __str__(self):
        return f'{self.comment_post.post_text[0:20]}: {self.comment_text}.{self.comment_user.username}'