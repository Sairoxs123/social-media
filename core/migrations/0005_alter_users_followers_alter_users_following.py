# Generated by Django 4.1.7 on 2024-01-20 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_files_remove_posts_photo_posts_files'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='followers', to='core.users'),
        ),
        migrations.AlterField(
            model_name='users',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='following', to='core.users'),
        ),
    ]