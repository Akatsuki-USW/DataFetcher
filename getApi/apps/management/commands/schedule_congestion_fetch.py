from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import os


def congestion_fetch():
    os.system('python3 manage.py congestion_fetch')
def daily_congestion_statistic():
    os.system('python3 manage.py daily_congestion_statistic')

def weekly_congestion_statisti():
    os.system('python3 manage.py weekly_congestion_statistic')

def sk_congestion_fetch():
    os.system('python3 manage.py sk_congestion_fetch')

class Command(BaseCommand):
    help = 'Runs a scheduler to fetch congestion data'

    def handle(self, *args, **options):
        scheduler = BackgroundScheduler()
        trigger1 = CronTrigger(minute="21", hour="9-23")
        scheduler.add_job(congestion_fetch, trigger1)

        trigger2 = CronTrigger(minute="30", hour="0")
        scheduler.add_job(daily_congestion_statistic, trigger2)

        trigger3 = CronTrigger(minute="30", hour="0", day_of_week="mon")
        scheduler.add_job(weekly_congestion_statisti, trigger3)

        trigger4 = CronTrigger(minute="21", hour="9-23")
        scheduler.add_job(sk_congestion_fetch, trigger4)

        scheduler.start()
        self.stdout.write(self.style.SUCCESS('스케줄러 시작'))

        try:
            while True:
                pass
        except KeyboardInterrupt:
            # 스케줄러 정지
            scheduler.shutdown()
            self.stdout.write(self.style.SUCCESS('스케줄러 끝'))
