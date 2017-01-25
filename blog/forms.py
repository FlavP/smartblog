from django.forms import ModelForm

from .models import Article

class ArticleForm(ModelForm):

    class Meta:
        model = Article
        fields = '__all__'

    def clean_art_slug(self):
        return self.cleaned_data['art_slug'].lower()


