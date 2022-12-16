# Generated by Django 4.1.4 on 2022-12-16 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('integrations', '0001_create_integration_and_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(help_text='Name of the category', max_length=32, unique=True),
        ),
        migrations.AddConstraint(
            model_name='integration',
            constraint=models.UniqueConstraint(fields=('name', 'category'), name='unique_name_and_category'),
        ),
    ]
