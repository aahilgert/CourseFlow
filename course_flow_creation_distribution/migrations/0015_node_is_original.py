# Generated by Django 2.2.6 on 2019-11-08 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_flow_creation_distribution', '0014_auto_20191107_2104'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='is_original',
            field=models.BooleanField(default=True),
        ),
    ]