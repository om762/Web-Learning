# Generated by Django 5.0.3 on 2024-04-17 13:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isbn', models.CharField(max_length=10)),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=80)),
                ('publication_year', models.IntegerField()),
                ('publisher', models.CharField(max_length=50)),
                ('image', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='BookReader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stared_reading', models.DateField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reading_book', to='books.book')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reading_by', to='books.person')),
            ],
        ),
    ]
