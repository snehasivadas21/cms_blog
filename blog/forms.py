from django import forms
from .models import Blog, Attachment

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title','content','is_published']

    def clean_title(self):
        title = self.cleaned_data['title']

        if len(title)<5:
            raise forms.ValidationError("Title must be at least 5 char")
        return title
    
    def clean_content(self):
        content = self.cleaned_data['content']

        if not content.strip():
            raise forms.ValidationError("Content required")
        return content

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file']