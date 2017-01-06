from django.db import models
import datetime

# Create your models here.
class Tag(models.Model):
    tagid = models.AutoField(
        primary_key=True,
        serialize=False,
        verbose_name='tagid',
        auto_created=True
    )
    tagname = models.CharField(max_length=31, unique=True)
    tag_slug = models.SlugField()
    added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.tagname.title()

    class Meta:
        ordering = ['tagname']

class Company(models.Model):
    companyid = models.AutoField(
        primary_key=True,
        serialize=False,
        verbose_name='compid',
        auto_created=True
    )
    company_name = models.CharField(max_length=31)
    company_slug = models.SlugField(max_length=31, unique=True, help_text="Label for URL composition")
    description = models.TextField()
    founded_date = models.DateField('date when it was founded')
    email = models.EmailField()
    website = models.URLField(max_length=255)
    added = models.DateField(auto_now_add=True)
    # It is entirely up to you where you define the many to many relationship, related_type --> the name
    # to refer from the other table to this one, like t.companies (t short for tags) or c.tags (c short for company)
    tags = models.ManyToManyField(Tag, related_name='companies')

    def __str__(self):
        return self.company_name

    class Meta:
        ordering = ['company_name']
        get_latest_by = 'founded_date'

class RelatedNews(models.Model):
    title = models.CharField(max_length=63)
    pub_date = models.DateField('date published')
    newslink = models.URLField(max_length=255)
    company = models.ForeignKey(Company)

    def __str__(self):
        #self.company calls the str (string) method of the company object
        return "{}:{}",format(self.company, self.title)

    class Meta:
        #verbose = change the display string of a class
        verbose_name = "related news"
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'
