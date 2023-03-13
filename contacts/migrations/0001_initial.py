# Generated by Django 4.1.2 on 2022-11-02 21:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
        ("sites", "0002_alter_domain_unique"),
    ]

    operations = [
        migrations.CreateModel(
            name="Contact",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "key",
                    models.CharField(
                        help_text="Key must be unique to all your contacts",
                        max_length=100,
                        verbose_name="key",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="This name will be used across informer app",
                        max_length=200,
                        verbose_name="name",
                    ),
                ),
                (
                    "index1",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="index 1"
                    ),
                ),
                (
                    "index2",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="index 2"
                    ),
                ),
                (
                    "index3",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="index 3"
                    ),
                ),
                (
                    "index4",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="index 4"
                    ),
                ),
                (
                    "index5",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="index 5"
                    ),
                ),
                (
                    "index6",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="index 6"
                    ),
                ),
                (
                    "contact_data",
                    models.JSONField(
                        default=dict,
                        help_text="Contact data will be available for use in flow templates",
                        verbose_name="contact data",
                    ),
                ),
                (
                    "channel_data",
                    models.JSONField(default=dict, verbose_name="channel data"),
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
                "verbose_name": "contact",
                "verbose_name_plural": "contacts",
            },
        ),
        migrations.AddIndex(
            model_name="contact",
            index=models.Index(
                fields=["environment", "index1"], name="contacts_co_environ_0451c4_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="contact",
            index=models.Index(
                fields=["environment", "index2"], name="contacts_co_environ_711e13_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="contact",
            index=models.Index(
                fields=["environment", "index3"], name="contacts_co_environ_058565_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="contact",
            index=models.Index(
                fields=["environment", "index4"], name="contacts_co_environ_007576_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="contact",
            index=models.Index(
                fields=["environment", "index5"], name="contacts_co_environ_e297c1_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="contact",
            index=models.Index(
                fields=["environment", "index6"], name="contacts_co_environ_de5957_idx"
            ),
        ),
        migrations.AddConstraint(
            model_name="contact",
            constraint=models.UniqueConstraint(
                models.F("environment"), models.F("key"), name="key_environment"
            ),
        ),
    ]
