from django.core.management import BaseCommand
from getApi.models import Congestion
from django.db.models import Avg
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = "weekly_congestion_statistic.py"
    def handle(self, *args, **options):
        relax_level = next(filter(lambda x: x[1]=="RELAX", Congestion.CONGESTION_LEVEL_CHOICES))[0]
        normal_level = next(filter(lambda x: x[1]=="NORMAL", Congestion.CONGESTION_LEVEL_CHOICES))[0]
        buzz_level = next(filter(lambda x: x[1]=="BUZZ", Congestion.CONGESTION_LEVEL_CHOICES))[0]

        # 이게 days=7인지 days=6인지 햇갈리네요 . >> 7일이 맞는걸로 확인.
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=7)

        result = (
            Congestion.objects
            .filter(observed_at__range=(start_date, end_date))
            .filter(congestion_level__in=[relax_level, normal_level, buzz_level])
            .values('location__name')
            .annotate(avg_congestion_level=Avg('congestion_level'))
        )

        for item in result:
            print(item['location__name'], item['avg_congestion_level'])
