# Generated by Django 4.1.3 on 2022-12-13 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True, verbose_name='Name')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
            ],
        ),
    ]