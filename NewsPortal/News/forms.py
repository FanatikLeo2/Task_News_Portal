from django import forms
from .models import Post, Comment
from django.core.exceptions import ValidationError


class PostCreateForm(forms.ModelForm):
    post_title = forms.CharField(min_length=5, label='Заголовок статьи')
    post_text = forms.CharField(min_length=20, label='Текст статьи')

    class Meta:
        model = Post
        fields = ['post_author', 'post_type', 'post_category', 'post_title', 'post_text']

    # def clean_name(self):
    #     post_text = self.cleaned_data["post_text"]
    #     if post_text[0].islower():
    #         raise ValidationError("Текст должен начинаться с заглавной буквы")
    #     return post_text


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
