# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-01-05 13:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('companyid', models.AutoField(primary_key=True, serialize=True)),
                ('company_name', models.CharField(max_length=31)),
                ('company_slug', models.SlugField(help_text='Label for URL composition', max_length=31, unique=True)),
                ('description', models.TextField()),
                ('founded_date', models.DateField(verbose_name='date when it was founded')),
                ('email', models.EmailField(max_length=254)),
                ('website', models.URLField(max_length=255)),
                ('added', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ['company_name'],
                'get_latest_by': 'founded_date',
            },
        ),
        migrations.CreateModel(
            name='RelatedNews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=63)),
                ('pub_date', models.DateField(verbose_name='date published')),
                ('newslink', models.URLField(max_length=255)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='centralizer.Company')),
            ],
            options={
                'ordering': ['-pub_date'],
                'verbose_name': 'related news',
                'get_latest_by': 'pub_date',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('tagid', models.AutoField(primary_key=True, serialize=False)),
                ('tagname', models.CharField(max_length=31, unique=True)),
                ('tag_slug', models.SlugField()),
                ('added', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ['tagname'],
            },
        ),
        migrations.AddField(
            model_name='company',
            name='tags',
            field=models.ManyToManyField(related_name='companies', to='centralizer.Tag'),
        ),
    ]
