# Generated by Django 4.0.4 on 2022-05-31 22:34

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0003_alter_channel_account'),
        ('pipelines', '0002_alter_pipeline_environments_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pipelinerun',
            name='trigger',
        ),
        migrations.AlterField(
            model_name='pipelinestep',
            name='order',
            field=models.PositiveSmallIntegerField(editable=False, verbose_name='order'),
        ),
        migrations.CreateModel(
            name='PipelineLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('pipeline_run_id', models.UUIDField(verbose_name='pipeline_run_id')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='date')),
                ('level', models.CharField(choices=[('debug', 'debug'), ('info', 'info'), ('warning', 'warning'), ('error', 'error')], default='info', max_length=10, verbose_name='level')),
                ('message', models.CharField(max_length=400, verbose_name='message')),
                ('context', models.JSONField(default=dict, verbose_name='context')),
                ('account', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='configuration.account', verbose_name='account')),
                ('environment', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='configuration.environment', verbose_name='environment')),
            ],
            options={
                'verbose_name': 'pipeline log',
                'verbose_name_plural': 'pipeline logs',
                'ordering': ('-date',),
            },
        ),
        migrations.AddIndex(
            model_name='pipelinelog',
            index=models.Index(fields=['pipeline_run_id', '-date'], name='pipelines_p_pipelin_edb0af_idx'),
        ),
    ]
