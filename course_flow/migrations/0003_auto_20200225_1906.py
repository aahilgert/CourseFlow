# Generated by Django 2.2.9 on 2020-02-25 19:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("course_flow", "0002_auto_20200219_2139"),
    ]

    operations = [
        migrations.AddField(
            model_name="activity",
            name="students",
            field=models.ManyToManyField(
                blank=True,
                related_name="assigned_activities",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="course",
            name="students",
            field=models.ManyToManyField(
                blank=True,
                related_name="assigned_courses",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="activity",
            name="author",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="authored_activities",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="course",
            name="author",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="authored_courses",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="node",
            name="author",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="authored_nodes",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="node",
            name="students",
            field=models.ManyToManyField(
                blank=True,
                related_name="assigned_nodes",
                through="course_flow.NodeCompletionStatus",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
