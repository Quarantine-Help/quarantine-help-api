# Generated by Django 3.0.4 on 2020-03-28 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [("crisis", "0001_initial"), ("management", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="requestassignment",
            name="assignee",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="management.Participant"
            ),
        ),
        migrations.AddField(
            model_name="requestassignment",
            name="request",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="crisis.Request"
            ),
        ),
        migrations.AddField(
            model_name="request",
            name="assignee",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="assignee",
                to="management.Participant",
            ),
        ),
        migrations.AddField(
            model_name="request",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="owner",
                to="management.Participant",
            ),
        ),
    ]