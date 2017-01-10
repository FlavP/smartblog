from django.db import models
from centralizer.models import Tag, Company
import datetime
# Create your models here.

class Article(models.Model):
    articleid = models.AutoField(
        primary_key=True,
        serialize=False,
        verbose_name='articleid',
        auto_created=True
    )
    title = models.CharField(max_length=63)
    #we check for uniqueness for articles published in the same monts
    art_slug = models.SlugField(
                                max_length=63,
                                help_text="Label for URL composition",
                                unique_for_month='added',
                                )
    content = models.TextField()
    added = models.DateField('date when the article was added', auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='articles')
    companies = models.ManyToManyField(Company, related_name='articles')

    def __str__(self):
        return "{} on {}".format(
            self.title,
            self.added.strftime("%Y-%m-%d")
        )

    class Meta:
        verbose_name = "blog article"
        ordering = ["-added", "title"]
        get_latest_by = 'added'
