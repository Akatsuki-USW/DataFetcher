from datetime import datetime, timedelta
from django.core.management import BaseCommand
from getApi.models import Congestion, DailyCongestionStatistic

class Command(BaseCommand):
    help = "daily_congestion_statistic.py"

    def handle(self, *args, **options):
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        yesterday_date = yesterday.date()

        unique_location_ids = Congestion.objects.filter(observed_at__date=yesterday_date).values_list('location_id', flat=True).distinct()

        for location_id in unique_location_ids:
            congestion_data = Congestion.objects.filter(observed_at__date=yesterday_date, location_id=location_id)

            statistics = []

            for congestion in congestion_data:
                observed_time = congestion.observed_at.strftime("%H")
                congestion_level = congestion.congestion_level
                print(f"Observed time: {observed_time}")  # 문제확인.

                statistics.append({
                    "time": int(observed_time),
                    "congestionLevel": congestion_level
                })

            print(statistics)

            statistic = DailyCongestionStatistic.objects.create(
                location_id=location_id,
                content={"statistics": statistics}
            )

            #statistic.save()

