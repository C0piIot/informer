# Generated by Django 4.1.2 on 2022-11-02 21:45

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("sites", "0002_alter_domain_unique"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Flow",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, verbose_name="id"
                    ),
                ),
                (
                    "revision",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="revision",
                    ),
                ),
                ("date", models.DateTimeField(
                    auto_now_add=True, verbose_name="date")),
                ("name", models.CharField(max_length=150, verbose_name="name")),
                ("enabled", models.BooleanField(
                    default=True, verbose_name="enabled")),
                (
                    "trigger",
                    models.CharField(
                        db_index=True, max_length=150, verbose_name="trigger"
                    ),
                ),
                (
                    "environments",
                    models.ManyToManyField(
                        editable=False, related_name="flows", to="accounts.environment"
                    ),
                ),
                (
                    "site",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="flows",
                        to="sites.site",
                        verbose_name="site",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "flow",
                "verbose_name_plural": "communication flows",
                "ordering": ("id", "-date"),
            },
        ),
        migrations.CreateModel(
            name="FlowStep",
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
                    "order",
                    models.PositiveSmallIntegerField(
                        editable=False, verbose_name="order"
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "flow",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="steps",
                        to="flows.flow",
                        verbose_name="flow",
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
                "verbose_name": "flow step",
                "verbose_name_plural": "flow steps",
                "ordering": ("flow", "order"),
                "unique_together": {("flow", "order")},
            },
        ),
        migrations.CreateModel(
            name="Delay",
            fields=[
                (
                    "flowstep_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="flows.flowstep",
                    ),
                ),
                ("time", models.DurationField(verbose_name="time")),
            ],
            options={
                "verbose_name": "delay",
                "verbose_name_plural": "delays",
            },
            bases=("flows.flowstep",),
        ),
        migrations.CreateModel(
            name="Email",
            fields=[
                (
                    "flowstep_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="flows.flowstep",
                    ),
                ),
                ("subject", models.CharField(max_length=200, verbose_name="subject")),
                ("html_body", models.TextField(verbose_name="html body message")),
                (
                    "text_body",
                    models.TextField(
                        help_text="Text used on clients that don't support html emails",
                        verbose_name="plain text message",
                    ),
                ),
                (
                    "autogenerate_text",
                    models.BooleanField(
                        default=True,
                        help_text="Generate text automatically from html template",
                        verbose_name="autogenerate text",
                    ),
                ),
                (
                    "from_email",
                    models.EmailField(
                        blank=True,
                        help_text="From address for this step. Overrides channel's default from address",
                        max_length=200,
                        verbose_name="from email",
                    ),
                ),
                (
                    "preview_context",
                    models.JSONField(
                        blank=True, default=dict, verbose_name="preview context"
                    ),
                ),
            ],
            options={
                "verbose_name": "send email",
                "verbose_name_plural": "email sending",
            },
            bases=("flows.flowstep",),
        ),
        migrations.CreateModel(
            name="Group",
            fields=[
                (
                    "flowstep_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="flows.flowstep",
                    ),
                ),
                ("window", models.DurationField(verbose_name="time window")),
                ("key", models.SlugField(max_length=150, verbose_name="grouping key")),
            ],
            options={
                "verbose_name": "group",
                "verbose_name_plural": "groupings",
            },
            bases=("flows.flowstep",),
        ),
        migrations.CreateModel(
            name="Push",
            fields=[
                (
                    "flowstep_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="flows.flowstep",
                    ),
                ),
                ("title", models.CharField(max_length=200, verbose_name="title")),
                ("body", models.TextField(verbose_name="body")),
                ("url", models.URLField(verbose_name="url")),
                (
                    "preview_context",
                    models.JSONField(
                        blank=True, default=dict, verbose_name="preview context"
                    ),
                ),
            ],
            options={
                "verbose_name": "send push",
                "verbose_name_plural": "push sending",
            },
            bases=("flows.flowstep",),
        ),
        migrations.CreateModel(
            name="Webhook",
            fields=[
                (
                    "flowstep_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="flows.flowstep",
                    ),
                ),
                ("url", models.URLField(verbose_name="url")),
                (
                    "method",
                    models.CharField(
                        choices=[
                            ("GET", "GET"),
                            ("POST", "POST"),
                            ("PUT", "PUT"),
                            ("PATCH", "PATCH"),
                            ("DELETE", "DELETE"),
                        ],
                        max_length=6,
                        verbose_name="method",
                    ),
                ),
                (
                    "contenttype",
                    models.CharField(
                        choices=[
                            (
                                "application/x-www-form-urlencoded",
                                "application/x-www-form-urlencoded",
                            ),
                            ("application/json", "application/json"),
                            ("application/xml", "application/xml"),
                            ("text/plain", "text/plain"),
                            ("text/html", "text/html"),
                        ],
                        max_length=50,
                        verbose_name="Content type",
                    ),
                ),
                ("body", models.TextField(blank=True, verbose_name="body")),
                (
                    "preview_context",
                    models.JSONField(
                        blank=True, default=dict, verbose_name="preview context"
                    ),
                ),
            ],
            options={
                "verbose_name": "webook",
                "verbose_name_plural": "webhooks",
            },
            bases=("flows.flowstep",),
        ),
        migrations.CreateModel(
            name="FlowRun",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="id",
                    ),
                ),
                (
                    "start",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="start"),
                ),
                ("flow_id", models.UUIDField(editable=False, verbose_name="id")),
                (
                    "contact_key",
                    models.CharField(
                        max_length=100, verbose_name="contact key"),
                ),
                (
                    "event_payload",
                    models.JSONField(
                        blank=True, default=dict, verbose_name="event payload"
                    ),
                ),
                ("flow_data", models.JSONField(
                    default=dict, verbose_name="flow data")),
                (
                    "group_key",
                    models.CharField(
                        blank=True,
                        editable=False,
                        max_length=200,
                        verbose_name="group_key",
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
                    "flow_revision",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="flows.flow",
                        verbose_name="flow",
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
                "verbose_name": "flow run",
                "verbose_name_plural": "flow runs",
                "ordering": ("-start",),
            },
        ),
        migrations.CreateModel(
            name="FlowLog",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="id",
                    ),
                ),
                ("flow_run_id", models.UUIDField(verbose_name="flow_run_id")),
                ("date", models.DateTimeField(
                    auto_now_add=True, verbose_name="date")),
                (
                    "level",
                    models.CharField(
                        choices=[
                            ("DEBUG", "debug"),
                            ("INFO", "info"),
                            ("WARNING", "warning"),
                            ("ERROR", "error"),
                        ],
                        default="INFO",
                        max_length=10,
                        verbose_name="level",
                    ),
                ),
                ("message", models.CharField(max_length=400, verbose_name="message")),
                ("context", models.JSONField(default=dict, verbose_name="context")),
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
                "verbose_name": "flow log",
                "verbose_name_plural": "flow logs",
                "ordering": ("date",),
            },
        ),
        migrations.AddConstraint(
            model_name="flowrun",
            constraint=models.UniqueConstraint(
                fields=("contact_key", "flow_revision", "group_key"),
                name="unique group",
            ),
        ),
        migrations.AddIndex(
            model_name="flowlog",
            index=models.Index(
                fields=["flow_run_id", "-date"], name="flows_flowl_flow_ru_05e9c6_idx"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="flow",
            unique_together={("id", "date")},
        ),
    ]
