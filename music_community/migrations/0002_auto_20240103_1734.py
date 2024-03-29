# Generated by Django 3.1.1 on 2024-01-03 17:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('music_community', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MusicCommunityCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(allow_unicode=True, max_length=200, unique=True)),
            ],
            options={
                'verbose_name_plural': 'MusicCommunityCategories',
            },
        ),
        migrations.CreateModel(
            name='MusicCommunityComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MusicCommunityPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('hook_text', models.CharField(blank=True, max_length=100)),
                ('content', markdownx.models.MarkdownxField()),
                ('head_image', models.ImageField(blank=True, upload_to='music_community/images/%Y/%m/%d/')),
                ('file_upload', models.FileField(blank=True, upload_to='music_community/files/%Y/%m/%d/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='music_community.musiccommunitycategory')),
            ],
        ),
        migrations.CreateModel(
            name='MusicCommunityTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(allow_unicode=True, max_length=200, unique=True)),
            ],
        ),
        migrations.DeleteModel(
            name='CommunityPost',
        ),
        migrations.AddField(
            model_name='musiccommunitypost',
            name='tags',
            field=models.ManyToManyField(blank=True, to='music_community.MusicCommunityTag'),
        ),
        migrations.AddField(
            model_name='musiccommunitycomment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music_community.musiccommunitypost'),
        ),
    ]
