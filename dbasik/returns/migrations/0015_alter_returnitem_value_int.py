# Generated by Django 4.0.3 on 2022-03-31 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('returns', '0014_alter_return_id_alter_returnitem_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='returnitem',
            name='value_int',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
