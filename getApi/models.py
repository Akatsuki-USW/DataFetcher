from django.db import models


class LocationCategory(models.Model):
    location_category_id = models.BigAutoField(primary_key=True)
    icon_image_url = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'location_category'

class Location(models.Model):
    location_id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    api_id = models.IntegerField()
    name = models.CharField(max_length=255, blank=True, null=True)
    location_category_id = models.ForeignKey(LocationCategory, on_delete=models.SET_NULL, null=True, blank=True, db_column='location_category_id')

    class Meta:
        managed = False
        db_table = 'location'

class Congestion(models.Model):
        CONGESTION_LEVEL_CHOICES = [
            (1,'RELAX'),
            (2,'NORMAL'),
            (3,'BUZZ'),
        ]

        congestion_id = models.BigAutoField(primary_key=True)
        created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
        updated_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
        congestion_level = models.IntegerField(choices=CONGESTION_LEVEL_CHOICES, blank=True, null=True)
        observed_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
        location = models.ForeignKey('Location', models.DO_NOTHING)

        class Meta:
            managed = False
            db_table = 'congestion'


class CongestionStatics(models.Model):
    congestion_statistics_id = models.BigAutoField(primary_key=True)
    location = models.ForeignKey('Location', models.DO_NOTHING)
    congestion = models.JSONField(blank=True, null=True)
    created_at = models.CharField(max_length=225)
    updated_at = models.CharField(max_length=225)

    class Meta:
        managed = False
        db_table = 'congestion_statics'

class DailyCongestionStatistic(models.Model):
    daily_congestion_statistic_id = models.BigAutoField(primary_key=True) # 이름변경됨.
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    content = models.JSONField(blank=True, null=True)
    location = models.ForeignKey('Location', models.DO_NOTHING)


    class Meta:
        managed = False
        db_table = 'daily_congestion_statistic'

class WeeklyCongestionStatistic(models.Model):
    weekly_congestion_statistic_id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    average_congestion_level = models.FloatField(blank=True, null=True)
    location = models.ForeignKey(Location, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'weekly_congestion_statistic'
