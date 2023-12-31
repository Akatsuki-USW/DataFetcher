# Generated by Django 4.2 on 2023-08-21 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ban',
            fields=[
                ('ban_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('ban_ended_at', models.DateTimeField(blank=True, null=True)),
                ('ban_started_at', models.DateTimeField(blank=True, null=True)),
                ('content', models.CharField(blank=True, max_length=300, null=True)),
                ('is_banned', models.TextField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'ban',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('report_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('content', models.CharField(blank=True, max_length=300, null=True)),
                ('report_target', models.CharField(blank=True, max_length=255, null=True)),
                ('target_id', models.BigIntegerField(blank=True, null=True)),
                ('ischecked', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'report',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('fcm_token', models.CharField(blank=True, max_length=255, null=True)),
                ('last_login_date', models.DateTimeField(blank=True, null=True)),
                ('nickname', models.CharField(blank=True, max_length=20, null=True)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('profile_image_url', models.CharField(blank=True, max_length=500, null=True)),
                ('role', models.CharField(blank=True, max_length=255, null=True)),
                ('social_email', models.CharField(blank=True, max_length=255, null=True)),
                ('social_type', models.CharField(blank=True, max_length=255, null=True)),
                ('user_status', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'users',
                'managed': False,
            },
        ),
    ]
