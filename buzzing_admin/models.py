from django.db import models

class Users(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    fcm_token = models.CharField(max_length=255, blank=True, null=True)
    last_login_date = models.DateTimeField(blank=True, null=True)
    nickname = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    profile_image_url = models.CharField(max_length=500, blank=True, null=True)
    role = models.CharField(max_length=255, blank=True, null=True)
    social_email = models.CharField(max_length=255, blank=True, null=True)
    social_type = models.CharField(max_length=255, blank=True, null=True)
    user_status = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'

class Ban(models.Model):
    ban_id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    ban_ended_at = models.DateTimeField(blank=True, null=True)
    ban_started_at = models.DateTimeField(blank=True, null=True)
    content = models.CharField(max_length=300, blank=True, null=True)
    is_banned = models.BooleanField(blank=True, null=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    banned_user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ban'


class Report(models.Model):
    report_id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    content = models.CharField(max_length=300, blank=True, null=True)
    report_target = models.CharField(max_length=255, blank=True, null=True)
    target_id = models.BigIntegerField(blank=True, null=True)
    ban = models.ForeignKey(Ban, models.DO_NOTHING, blank=True, null=True)
    reported_user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    reporter_user = models.ForeignKey('Users', models.DO_NOTHING, related_name='report_reporter_user_set', blank=True, null=True)
    ischecked = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'report'

class BlackList(models.Model):
    black_list_id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    ban_ended_at = models.DateTimeField(blank=True, null=True)
    ban_started_at = models.DateTimeField(blank=True, null=True)
    social_email = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'black_list'
