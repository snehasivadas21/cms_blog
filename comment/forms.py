from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

    def clean_comment(self):
        comment = self.cleaned_data['comment']

        if not comment:
            raise forms.ValidationError("comment required")

        if len(comment)<3:
            raise forms.ValidationError("comment atlease 3 char needed")
        return comment    