from django import forms
from .models import Community, Comment


class CommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        # fields = '__all__'

        exclude = ['user', 'hits', 'like_users',
                   'recommend_users', 'date', 'content']


class CommentForm(forms.ModelForm):
    content = forms.CharField(label=False)

    class Meta:
        model = Comment
        #fields = '__all__'

        exclude = ['article', 'user', 'comment_select_users']
