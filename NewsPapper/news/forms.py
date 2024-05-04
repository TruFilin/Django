from django import forms
from .models import Post
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'categories', 'created_at', 'content', 'author']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("title")
        description = cleaned_data.get("content")

        if name == description:
            raise ValidationError("Описание не должно быть идентично названию.")

        return cleaned_data
