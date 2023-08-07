from datetime import date, timedelta
from django.core.management import BaseCommand
from getApi.models import Congestion, DailyCongestionStatistic

class Command(BaseCommand):
    help = "daily_congestion_statistic.py"

    def handle(self, *args, **options):
        today = date.today()
        yesterday = today - timedelta(days=1)

        unique_location_ids = Congestion.objects.filter(observed_at__date=yesterday).values_list('location_id', flat=True).distinct()

        for location_id in unique_location_ids:
            congestion_data = Congestion.objects.filter(observed_at__date=yesterday, location_id=location_id)
            statistics = []

            for congestion in congestion_data:
                observed_date = congestion.observed_at.strftime("%Y-%m-%d")
                observed_time = congestion.observed_at.strftime("%H")
                congestion_level = congestion.congestion_level

                statistics.append({
                    "time": int(observed_time),
                    "congestionLevel": congestion_level
                })

            statistic = DailyCongestionStatistic.objects.filter(location_id=location_id).first()

            if statistic is None:
                statistic = DailyCongestionStatistic.objects.create(
                    location_id=location_id,
                    content={"statistics": statistics}
                )
            else:
                statistic.content["statistics"] = statistics

            statistic.save()
