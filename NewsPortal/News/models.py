from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import reverse
from django.core.cache import cache


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


    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return f'{self.category_name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    NEWS = 'NE'
    ARTICLE = 'AR'
    POSTTYPES = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    ]

    post_author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    post_type = models.CharField(max_length=2, choices=POSTTYPES, default=NEWS, verbose_name='Тип поста')
    post_time_in = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    post_category = models.ManyToManyField(Category, through='PostCategory', verbose_name='Категория поста')
    post_title = models.CharField(max_length=255, verbose_name='Заголовок')
    post_text = models.TextField(verbose_name='Текст')
    post_rating = models.FloatField(default=0, verbose_name='Рейтинг')

    @property
    def in_rating(self):
        if self.post_rating > 0:
            return self.post_rating

    def __str__(self):
        return f'{self.post_title[0:50]}... {self.post_text[0:50]}...'

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return f'{self.post_text[0:123]} ...'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    # def save(self, *args, **kwargs):    разобраться с кешированием
    #     super().save(*args, **kwargs)
    #     cache.delete(f'post-{self.pk}')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-post_time_in']


class PostCategory(models.Model):
    post_through = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_through = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE,verbose_name='Пост коментария')
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='Автор коментария')
    comment_text = models.TextField(verbose_name='Текст коментария')
    comment_time_in = models.DateTimeField(auto_now_add=True)
    comment_rating = models.FloatField(default=0, verbose_name='Ретинг')

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()

    def __str__(self):
        return f'{self.comment_text} {self.comment_user.username} ------ {self.comment_post.post_text[0:50]}...'

    def get_absolute_url(self):
        return reverse('show_comment', kwargs={'comment_text': self.comment_text})

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'
        ordering = ['comment_time_in']


# class Subscription(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions', verbose_name='Пользователь подписки')
#     category = models.ForeignKey(to='Category', on_delete=models.CASCADE, related_name='subscriptions', verbose_name='Подписка')