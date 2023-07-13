from datetime import date, timedelta
from django.core.management import BaseCommand
from getApi.models import Congestion, DailyCongestionStatistic

class Command(BaseCommand):
    help = "daily_congestion_statistic.py"

    def handle(self, *args, **options):
        today = date.today()
        yesterday = today - timedelta(days=1)

        congestion_data = Congestion.objects.filter(observed_at__date=yesterday)

        for congestion in congestion_data:
            location_id = congestion.location_id
            observed_date = congestion.observed_at.strftime("%Y-%m-%d")
            observed_time = congestion.observed_at.strftime("%H")
            congestion_level = congestion.congestion_level

            statistics = [
                {
                    "time": int(observed_time),
                    "congestionLevel": congestion_level
                }
            ]

            # 이미 존재하는 DailyCongestionStatistic 레코드를 가져옵니다.
            statistic = DailyCongestionStatistic.objects.filter(location_id=location_id, content__observedDate=observed_date).first()

            if statistic is None:
                statistic = DailyCongestionStatistic.objects.create(
                    location_id=location_id,
                    content={
                        "id": location_id,
                        "observedDate": observed_date,
                        "statistics": statistics
                    }
                )
            else:
                statistic.content["statistics"] += statistics

            statistic.save()
