# Generated by Django 4.1.7 on 2024-01-20 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_users_followers_alter_users_following'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='followers',
        ),
        migrations.RemoveField(
            model_name='users',
            name='following',
        ),
        migrations.CreateModel(
            name='FollowSystem',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='core.users')),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='core.users')),
            ],
        ),
    ]
