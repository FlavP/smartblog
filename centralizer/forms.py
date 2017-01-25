from django.forms import ModelForm
from .models import Tag, Company, RelatedNews
from django.core.exceptions import ValidationError

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


class NewsForm(ModelForm):
    class Meta:
        model = RelatedNews
        fields = '__all__'

    def clean_title(self):
        return self.cleaned_data['title'].lower()