# Generated by Django 4.2.4 on 2023-09-02 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_alter_post_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=models.TextField(verbose_name='متن مقاله'),
        ),
    ]
