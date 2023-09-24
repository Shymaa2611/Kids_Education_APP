# Generated by Django 4.1.10 on 2023-09-24 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0002_content_challenge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='content',
            field=models.ManyToManyField(blank=True, null=True, to='Api.content'),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='challenges/'),
        ),
    ]
