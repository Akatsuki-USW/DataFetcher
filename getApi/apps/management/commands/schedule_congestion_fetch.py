from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import os


def congestion_fetch():
    os.system('python3 manage.py congestion_fetch')

class Command(BaseCommand):
    help = 'Runs a scheduler to fetch congestion data'

    def handle(self, *args, **options):
        scheduler = BackgroundScheduler()
        trigger = CronTrigger(minute="0", hour="9-24")
        scheduler.add_job(congestion_fetch, trigger)
        scheduler.start()
        self.stdout.write(self.style.SUCCESS('스케줄러 시작'))

        try:
            while True:
                pass
        except KeyboardInterrupt:
            # 스케줄러 정지
            scheduler.shutdown()
            self.stdout.write(self.style.SUCCESS('스케줄러 끝'))
