# Generated by Django 4.2.6 on 2023-11-04 04:55

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='image_post/', verbose_name='Picture')),
                ('caption', models.CharField(blank=True, max_length=100000, null=True, verbose_name='Caption')),
                ('posted', models.DateTimeField(auto_now_add=True)),
                ('likes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Tag')),
                ('slug', models.SlugField(default=uuid.uuid1, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Stream_Following', to='accounts.userntfriend')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='news.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Stream_user', to='accounts.userntfriend')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='tag',
            field=models.ManyToManyField(blank=True, null=True, related_name='tags', to='news.tag'),
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.userntfriend'),
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Follower', to='accounts.userntfriend')),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Following', to='accounts.userntfriend')),
            ],
        ),
    ]
