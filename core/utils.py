from django.views.generic import UpdateView as UpViews

class UpdateView(UpViews):

    template_name_suffix = '_update_form'

