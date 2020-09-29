from django import forms
from .models import Comment


class Send(forms.Form):
    name = forms.CharField(max_length=225)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentF(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
