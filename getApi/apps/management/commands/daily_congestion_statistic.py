from datetime import date, timedelta
from django.core.management import BaseCommand
from getApi.models import Congestion

class Command(BaseCommand):
    help = "daily_congestion_statistic.py"

    def handle(self, *args, **options):
        today = date.today()
        yesterday = today - timedelta(days=6)

        congestion_data = Congestion.objects.filter(observed_at__date=yesterday)

        #통계 데이터를 담을 딕셔너리
        statistics_dict = {}

        for congestion in congestion_data:
            location_id = congestion.location_id
            observed_date = congestion.observed_at.strftime("%Y-%m-%d")
            observed_time = congestion.observed_at.strftime("%H")
            congestion_level = congestion.congestion_level

            #딕셔너리에 해당 location_id가 없다면 추가
            if location_id not in statistics_dict:
                statistics_dict[location_id] = {
                    "id": location_id,
                    "observedDate": observed_date,
                    "statistics": []
                }

            #location_id의 통계 데이터에 추가
            statistics_dict[location_id]["statistics"].append({
                "time": int(observed_time),
                "congestionLevel": congestion_level
            })


        json_data = {"data": list(statistics_dict.values())}
        print(json_data)
