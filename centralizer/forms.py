from django.forms import ModelForm
from .models import Tag, Company, RelatedNews
from django.core.exceptions import ValidationError
from django.forms.widgets import HiddenInput

#importam modelele si le traducem in obiecte-formular echivalente
# in Meta definim ce model si ce campuri ale acelui model sunt folosite de un anume formular

class SlugMixin():
#A class mixin for the clean_slug for tag and company method
    def clean_slug(self):
        slug = (self.cleaned_data['elem_slug'].lower())
        if slug == "create":
            raise ValidationError("You can't give the slug the name 'create' !")
        return slug

class TagForms(ModelForm, SlugMixin):
    class Meta:
        model = Tag
        fields = "__all__"

    def clean_tagname(self):
        return self.cleaned_data['tagname'].lower()



class CompanyForms(ModelForm, SlugMixin):
    class Meta:
        model = Company
        fields = '__all__'

    def clean_company_name(self):
        return self.cleaned_data['company_name'].lower()


class NewsForm(ModelForm, SlugMixin):
    class Meta:
        model = RelatedNews
        fields = '__all__'
        widgets = {'company': HiddenInput()}

    def clean_title(self):
        return self.cleaned_data['title'].lower()

    def save(self, **kwargs):
        '''
        company_obj = kwargs.get('company_obj', None)
        if company_obj is not None:
            instance = super().save(commit=False)
            instance.company = company_obj
            instance.save()
            self.save_m2m()
        else:
            instance = super().save()
        return instance
        '''
        instance = super().save(commit=False)
        instance.company = (self.data.get('company'))
        instance.save()
        self.save_m2m()
        return instance

    def clean(self):
        cleaned_data = super().clean()
        news_slug = cleaned_data.get('news_slug')
        company_obj = self.data.get('company')
        isthere = (RelatedNews.objects.filter(news_slug__iexact=news_slug, company=company_obj).exists())
        if isthere:
            raise ValidationError("This entrance is already in the database")
        else:
            return cleaned_data