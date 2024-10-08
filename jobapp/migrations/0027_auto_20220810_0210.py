# Generated by Django 3.0 on 2022-08-09 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0026_auto_20220810_0156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='address',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='mobile',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='address',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='mobile',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='salary',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
