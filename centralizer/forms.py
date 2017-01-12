from django import forms
from .models import Tag, Company, RelatedNews
from django.core.exceptions import ValidationError

class SlugMixin():
#A class mixin for the clean_slug for tag and company method
    def clean_slug(self):
        slug = (self.cleaned_data['elem_slug'].lower())
        if slug == "create":
            raise ValidationError("You can't give the slug the name 'create' !")
        return slug

class TagForms(forms.ModelForm, SlugMixin):
    def Meta(self):
        model = Tag
        fields = "__all__"

    def clean_tagname(self):
        return self.cleaned_data['tagname'].lower()



class CompanyForms(forms.ModelForm, SlugMixin):
    def Meta(self):
        model = Company
        fields = '__all__'

    def clean_company_name(self):
        return self.cleaned_data['company_name'].lower()


class NewsForm(forms.ModelForm):
    def Meta(self):
        model = RelatedNews
        fields = '__all__'

    def clean_title(self):
        return self.cleaned_data['title'].lower()