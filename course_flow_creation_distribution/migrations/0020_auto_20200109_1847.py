# Generated by Django 2.2.8 on 2020-01-09 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("course_flow_creation_distribution", "0019_auto_20191128_2245")]

    operations = [
        migrations.AlterField(
            model_name="node",
            name="activity_classification",
            field=models.PositiveIntegerField(
                choices=[
                    (1, "Gather Information"),
                    (2, "Discuss"),
                    (3, "Solve"),
                    (4, "Analyze"),
                    (5, "Assess/Review Papers"),
                    (6, "Evaluate Peers"),
                    (7, "Debate"),
                    (8, "Game/Roleplay"),
                    (9, "Create/Design"),
                    (10, "Revise/Improve"),
                    (11, "Read"),
                    (12, "Write"),
                    (13, "Present"),
                    (14, "Experiment/Inquiry"),
                    (15, "Quiz/Test"),
                    (16, "Other"),
                ],
                default=0,
            ),
        ),
        migrations.AlterField(
            model_name="node",
            name="work_classification",
            field=models.PositiveIntegerField(
                choices=[
                    (1, "Individual Work"),
                    (2, "Work in Groups"),
                    (3, "Whole Class"),
                ],
                default=2,
            ),
        ),
    ]