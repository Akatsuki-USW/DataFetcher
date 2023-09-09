from django.db import models
from getApi.models import Location

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
    is_checked = models.BooleanField(blank=True, null=True)

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

class Spot(models.Model):
    spot_id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    content = models.CharField(max_length=1500)
    road_name_address = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=50)
    location = models.ForeignKey(Location, models.DO_NOTHING)
    spot_category = models.ForeignKey('SpotCategory', models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'spot'

class Comment(models.Model):
    comment_id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    content = models.CharField(max_length=300)
    presence = models.TextField()  # This field type is a guess.
    parent_comment = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    spot = models.ForeignKey('Spot', models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'comment'

class SpotCategory(models.Model):
    spot_category_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'spot_category'
