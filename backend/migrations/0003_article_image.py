# Generated by Django 4.1.1 on 2022-09-27 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_article_alternative_names_article_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
