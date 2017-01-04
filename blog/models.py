from django.db import models
import datetime
# Create your models here.

class Article(models.Model):
    articleid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=63)
    art_slug = models.SlugField()
    content = models.TextField()
    pub_date = models.DateField()
    added = models.DateField(default = datetime.now, blank = False)


