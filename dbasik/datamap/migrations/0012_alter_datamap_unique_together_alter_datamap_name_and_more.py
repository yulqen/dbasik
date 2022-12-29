# Generated by Django 4.0.8 on 2022-11-17 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamap', '0011_alter_datamap_tier'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='datamap',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='datamap',
            name='name',
            field=models.CharField(max_length=25, unique=True),
        ),
        migrations.RemoveField(
            model_name='datamap',
            name='tier',
        ),
    ]