from datetime import date, timedelta
from django.core.management import BaseCommand
from getApi.models import Congestion, DailyCongestionStatistic

class Command(BaseCommand):
    help = "daily_congestion_statistic.py"

    def handle(self, *args, **options):
        today = date.today()
        yesterday = today - timedelta(days=3)

        congestion_data = Congestion.objects.filter(observed_at__date=yesterday)

        location_dict = {} #누적해서 저장하기위해 만듬.
        for congestion in congestion_data:
            location_id = congestion.location_id
            observed_date = congestion.observed_at.strftime("%Y-%m-%d")
            observed_time = congestion.observed_at.strftime("%H")
            congestion_level = congestion.congestion_level

            if location_id in location_dict:
                location_dict[location_id]['statistics'].append({
                    "time": int(observed_time),
                    "congestionLevel": congestion_level
                })
            else:
                location_dict[location_id] = {
                    "id": location_id,
                    "observedDate": observed_date,
                    "statistics": [
                        {
                            "time": int(observed_time),
                            "congestionLevel": congestion_level
                        }
                    ]
                }

        for location_id, content in location_dict.items():
            statistic = DailyCongestionStatistic(
                location_id=location_id,
                content=content
            )
            statistic.save()
