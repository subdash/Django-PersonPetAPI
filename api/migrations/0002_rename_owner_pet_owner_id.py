# Generated by Django 3.2.3 on 2021-05-21 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pet',
            old_name='owner',
            new_name='owner_id',
        ),
    ]
