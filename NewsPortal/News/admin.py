from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin
# from django.contrib.flatpages.admin import FlatPageAdmin
# from django.contrib.flatpages.models import FlatPage
# from django.utils.translation import gettext_lazy as _

# class FlatPageAdmin(FlatPageAdmin):
#     fieldsets = (
#         (None, {'fields': ('url', 'title', 'content', 'sites')}),
#         (_('Advanced options'), {
#             'classes': ('collapse',),
#             'fields': (
#                 'enable_comments',
#                 'registration_required',
#                 'template_name',
#             ),
#         }),
#     )


# напишем уже знакомую нам функцию обнуления товара на складе
def nullfy_rating(modeladmin, request, queryset): # все аргументы уже должны быть вам знакомы, самые нужные из них это request — объект хранящий информацию о запросе и queryset — грубо говоря набор объектов, которых мы выделили галочками.
    queryset.update(post_rating=0)
nullfy_rating.short_description = 'Обнулить рейтинг' # описание для более понятного представления в админ панеле задаётся, как будто это объект


class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('post_time_in', 'post_title', 'post_author', 'in_rating', 'post_rating') # генерируем список имён всех полей для более красивого отображения
    list_filter = ('post_author',)  # добавляем примитивные фильтры в нашу админку
    search_fields = ('post_author',)  # тут всё очень похоже на фильтры из запросов в базу
    actions = [nullfy_rating]  # добавляем действия в список


class CommentAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('comment_time_in', 'comment_post', 'comment_text', 'comment_user', 'comment_rating') # генерируем список имён всех полей для более красивого отображения
    list_filter = ('comment_user',)  # добавляем примитивные фильтры в нашу админку
    search_fields = ('comment_user',)  # тут всё очень похоже на фильтры из запросов в базу


class CategoryAdmin(TranslationAdmin):
    model = Category


class PostTransAdmin(TranslationAdmin):
    model = Post


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Author)
admin.site.register(Category)

# admin.site.unregister(FlatPage)
# admin.site.register(FlatPage, FlatPageAdmin)
