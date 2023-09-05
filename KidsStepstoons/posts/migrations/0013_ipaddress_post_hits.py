# Generated by Django 4.2.4 on 2023-09-05 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_alter_category_slug_alter_category_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='IPAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(verbose_name='آدرس آی\u200cپی')),
            ],
            options={
                'verbose_name': 'آدرس آی\u200cپی',
                'verbose_name_plural': 'آدرس\u200cهای آی\u200cپی',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='hits',
            field=models.ManyToManyField(blank=True, related_name='hits', to='posts.ipaddress', verbose_name='بازدید'),
        ),
    ]
