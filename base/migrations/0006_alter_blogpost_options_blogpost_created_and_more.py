# Generated by Django 4.2.3 on 2023-08-08 18:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0005_remove_topic_experts"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="blogpost",
            options={"ordering": ["-updated", "-created"]},
        ),
        migrations.AddField(
            model_name="blogpost",
            name="created",
            field=models.DateTimeField(auto_now_add=True, default='2012-01-01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="blogpost",
            name="topic",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, to="base.topic"
            ),
        ),
        migrations.AddField(
            model_name="blogpost",
            name="updated",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="experts",
            field=models.ManyToManyField(
                blank=True, related_name="experts", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="connections",
            field=models.ManyToManyField(
                blank=True, related_name="connections", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
