from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import os


def congestion_fetch():
    os.system('python3 manage.py congestion_fetch')
def daily_congestion_statistic():
    os.system('python3 manage.py daily_congestion_statistic')

class Command(BaseCommand):
    help = 'Runs a scheduler to fetch congestion data'

    def handle(self, *args, **options):
        scheduler = BackgroundScheduler()
        trigger1 = CronTrigger(minute="21", hour="9-23")
        scheduler.add_job(congestion_fetch, trigger1)

        trigger2 = CronTrigger(minute="30", hour="0", day_of_week="mon")
        scheduler.add_job(daily_congestion_statistic, trigger2)

        scheduler.start()
        self.stdout.write(self.style.SUCCESS('스케줄러 시작'))

        try:
            while True:
                pass
        except KeyboardInterrupt:
            # 스케줄러 정지
            scheduler.shutdown()
            self.stdout.write(self.style.SUCCESS('스케줄러 끝'))
