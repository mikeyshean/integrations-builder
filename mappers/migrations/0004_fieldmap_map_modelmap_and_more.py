# Generated by Django 4.1.4 on 2022-12-22 19:17

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mappers', '0003_transformer_remove_field_mappers_field_type_valid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FieldMap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ModelMap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveConstraint(
            model_name='field',
            name='unique_model_and_field_name',
        ),
        migrations.RemoveField(
            model_name='field',
            name='target_field',
        ),
        migrations.RemoveField(
            model_name='field',
            name='transformer',
        ),
        migrations.RemoveField(
            model_name='model',
            name='is_remote',
        ),
        migrations.RemoveField(
            model_name='model',
            name='target_model',
        ),
        migrations.AddConstraint(
            model_name='field',
            constraint=models.UniqueConstraint(fields=('model', 'name'), name='unique_model_and_field_name'),
        ),
        migrations.AddField(
            model_name='modelmap',
            name='map',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='mappers.map'),
        ),
        migrations.AddField(
            model_name='modelmap',
            name='source_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='mappers.model'),
        ),
        migrations.AddField(
            model_name='modelmap',
            name='target_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='mappers.model'),
        ),
        migrations.AddField(
            model_name='map',
            name='source_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='mappers.model'),
        ),
        migrations.AddField(
            model_name='map',
            name='target_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='mappers.model'),
        ),
        migrations.AddField(
            model_name='fieldmap',
            name='map',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='mappers.map'),
        ),
        migrations.AddField(
            model_name='fieldmap',
            name='source_field',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='mappers.field'),
        ),
        migrations.AddField(
            model_name='fieldmap',
            name='target_field',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='mappers.field'),
        ),
        migrations.AddField(
            model_name='fieldmap',
            name='transformer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='mappers.transformer'),
        ),
        migrations.AddConstraint(
            model_name='modelmap',
            constraint=models.UniqueConstraint(fields=('source_model', 'map', 'target_model'), name='mappers_modelmap_unique_source_map_target'),
        ),
        migrations.AddConstraint(
            model_name='map',
            constraint=models.UniqueConstraint(fields=('source_model', 'target_model'), name='unique_source_and_target'),
        ),
        migrations.AddConstraint(
            model_name='fieldmap',
            constraint=models.UniqueConstraint(fields=('source_field', 'map', 'target_field'), name='mappers_fieldmap_unique_source_map_target'),
        ),
    ]
