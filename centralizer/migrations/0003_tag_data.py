# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-27 22:31
from __future__ import unicode_literals

from django.db import migrations

TAGS = (
    ("Mobile", "mobile"),
    ("Web", "web"),
    ("Machine Learning", "machine-learning")
    )

def add_tag(apps, schema_editor):
    Tag = apps.get_model(
        'centralizer', 'Tag'
        )
    for tag_name, tag_slug in TAGS:
        new_tag = Tag.objects.create(
            tagname = tag_name,
            tag_slug = tag_slug
            )
                    
def remove_tag(apps, schema_editor):
    Article = apps.get_model(
        'blog', 'Article'
        )
    for art in ARTICLES:
        delart = Article.objects.get(art_slug=art['art_slug'])
        delart.delete()

class Migration(migrations.Migration):

    dependencies = [
        ('centralizer', '0002_new'),
    ]

    operations = [
        migrations.RunPython(
            add_tag,
            remove_tag
            )
    ]
