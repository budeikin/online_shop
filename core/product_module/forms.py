from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body', 'rate']


class ReplyCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
