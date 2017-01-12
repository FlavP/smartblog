from django import forms

from .models import Article

class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = '__all__'

    def clean_art_slug(self):
        return self.cleaned_data['art_slug'].lower()


