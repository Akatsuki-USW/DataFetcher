# api_server/getApi/apps/management/commands/schedule_congestion_fetch.py

from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os


def congestion_fetch():
    os.system('python3 manage.py congestion_fetch')

class Command(BaseCommand):
    help = 'Runs a scheduler to fetch congestion data'

    def handle(self, *args, **options):
        scheduler = BackgroundScheduler()
        scheduler.add_job(congestion_fetch, 'interval', hours=1)
        scheduler.start()
        self.stdout.write(self.style.SUCCESS('스케줄러 시작'))

        try:
            while True:
                pass
        except KeyboardInterrupt:
            # 스케줄러 정지
            scheduler.shutdown()
            self.stdout.write(self.style.SUCCESS('스케줄러 끝'))
