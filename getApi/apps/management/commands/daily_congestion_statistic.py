from datetime import datetime, timedelta
from django.core.management import BaseCommand
from getApi.models import Congestion, DailyCongestionStatistic
from django.db.models import Avg



class Command(BaseCommand):
    help = "daily_congestion_statistic.py"

    def handle(self, *args, **options):
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        yesterday_date = yesterday.date()

        unique_location_ids = Congestion.objects.filter(observed_at__date=yesterday_date).values_list('location_id',
                                                                                                      flat=True).distinct()

        for location_id in unique_location_ids:
            hourly_averages = {}
            for hour in range(24):
                hour_start = datetime(yesterday.year, yesterday.month, yesterday.day, hour, 0)
                hour_end = datetime(yesterday.year, yesterday.month, yesterday.day, hour, 59, 59)

                hourly_data = Congestion.objects.filter(
                    observed_at__range=(hour_start, hour_end),
                    location_id=location_id
                )

                # 평균 계산
                if hourly_data.exists():
                    avg_congestion = hourly_data.aggregate(Avg('congestion_level'))['congestion_level__avg']
                    hourly_averages[hour] = round(avg_congestion)

            statistics = [{"time": hour, "congestionLevel": congestion_level} for hour, congestion_level in
                          hourly_averages.items()]

            print(statistics)

            statistic = DailyCongestionStatistic.objects.create(
                location_id=location_id,
                content={"statistics": statistics}
            )

            statistic.save()
