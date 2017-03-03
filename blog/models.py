from django.db import models
from centralizer.models import Tag, Company
from django.core.urlresolvers import reverse
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
    tags = models.ManyToManyField(Tag, related_name='articles', blank=True)
    companies = models.ManyToManyField(Company, related_name='articles', blank=True)

    def __str__(self):
        return "{} on {}".format(
            self.title,
            self.added.strftime("%Y-%m-%d")
        )
    # this is our invention, it is not a method that Dkango looks for convention, like get_absolute_url

    def get_update_url(self):
        return reverse('blog_article_update',
                       kwargs={
                           'year': self.added.year,
                           'month': self.added.month,
                           'slug': self.art_slug})

    def get_absolute_url(self):
        #la reverse ai nevoie ori de kwargs, ori de pk
        return reverse("blog_article_details",
                       kwargs={
                           "year": self.added.year,
                           "month": self.added.month,
                           "slug": self.art_slug})

    def get_delete_url(self):
        return reverse('blog_article_delete',
                       kwargs={
                           'year': self.added.year,
                           'month': self.added.month,
                           'slug': self.art_slug})
        
    def get_yearly_archive_url(self):
        return reverse('yearly_archive', kwargs={'year': self.added.year})

    def get_monthly_archive_url(self):
        return reverse('monthly_archive', kwargs={'year': self.added.year, 'month': self.added.month})

    class Meta:
        verbose_name = "blog article"
        ordering = ["-added", "title"]
        get_latest_by = 'added'
        permissions = (
            ("view_future_article",
             "Can view unpublished Article"),)
