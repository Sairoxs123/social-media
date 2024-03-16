# Generated by Django 4.1.7 on 2024-01-20 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_users_public_alter_posts_likes_alter_users_followers_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('file', models.FileField(upload_to='posts/')),
            ],
        ),
        migrations.RemoveField(
            model_name='posts',
            name='photo',
        ),
        migrations.AddField(
            model_name='posts',
            name='files',
            field=models.ManyToManyField(to='core.files'),
        ),
    ]