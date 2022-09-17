# Generated by Django 3.2 on 2022-09-15 16:35

from django.db import migrations, models
import django_lifecycle.mixins
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_delete_demomodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='DemoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False, editable=False)),
                ('name', models.CharField(max_length=15)),
                ('number', models.PositiveSmallIntegerField()),
            ],
            options={
                'verbose_name': 'Demo',
                'verbose_name_plural': 'Demos',
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
    ]
