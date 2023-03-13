# Generated by Django 4.1.3 on 2022-12-07 17:13

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("sites", "0002_alter_domain_unique"),
        ("accounts", "0002_alter_environment_private_key_and_more"),
        ("contacts", "0005_remove_contact_public_key_contact_auth_key"),
    ]

    operations = [
        migrations.CreateModel(
            name="InboxEntry",
            fields=[
                (
                    "key",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="key",
                    ),
                ),
                ("date", models.DateTimeField(
                    auto_now_add=True, verbose_name="date")),
                ("title", models.CharField(max_length=100, verbose_name="title")),
                ("message", models.TextField(verbose_name="message")),
                ("url", models.URLField(blank=True, default="", verbose_name="url")),
                (
                    "read",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="read"),
                ),
                (
                    "entry_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        help_text="Additional data for custom implementations",
                        verbose_name="entry data",
                    ),
                ),
                (
                    "contact",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="contacts.contact",
                        verbose_name="contact",
                    ),
                ),
                (
                    "environment",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="accounts.environment",
                        verbose_name="environment",
                    ),
                ),
                (
                    "site",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="sites.site",
                        verbose_name="site",
                    ),
                ),
            ],
            options={
                "verbose_name": "inbox entry",
                "verbose_name_plural": "inbox entries",
                "ordering": ("-date",),
            },
        ),
        migrations.AddIndex(
            model_name="inboxentry",
            index=models.Index(
                fields=["site", "environment", "contact", "-date"],
                name="inbox_inbox_site_id_edc2c0_idx",
            ),
        ),
    ]
