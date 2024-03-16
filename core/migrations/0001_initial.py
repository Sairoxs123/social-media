# Generated by Django 4.1.7 on 2024-01-11 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('username', models.CharField(max_length=30, verbose_name='Userame')),
                ('email', models.EmailField(max_length=50, verbose_name='User Email')),
                ('password', models.CharField(max_length=30, verbose_name='Password')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='pfps/')),
                ('followers', models.ManyToManyField(blank=True, null=True, to='core.users')),
                ('following', models.ManyToManyField(blank=True, null=True, to='core.users')),
            ],
        ),
    ]