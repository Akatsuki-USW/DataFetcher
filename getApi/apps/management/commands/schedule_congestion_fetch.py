from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import os
import threading

def run_management_command(command_name):
    os.system(f'python3 manage.py {command_name}')

class Command(BaseCommand):
    help = 'schedule_congestion_fetch'

    def handle(self, *args, **options):
        scheduler = BackgroundScheduler()

        jobs = [
            {"function": "congestion_fetch", "minute": "21", "hour": "9-23"},
            {"function": "daily_congestion_statistic", "minute": "30", "hour": "0"},
            {"function": "weekly_congestion_statisti", "minute": "30", "hour": "0", "day_of_week": "mon"},
            {"function": "sk_congestion_fetch", "minute": "21", "hour": "9-23"}
        ]

        for job in jobs:
            trigger = CronTrigger(**{key: job.get(key) for key in ['minute', 'hour', 'day_of_week'] if job.get(key)})
            scheduler.add_job(run_management_command, trigger, kwargs={"command_name": job["function"]})

        scheduler.start()
        self.stdout.write(self.style.SUCCESS('스케줄러 시작'))

        try:
            threading.Event().wait()
        except KeyboardInterrupt:
            scheduler.shutdown()
            self.stdout.write(self.style.SUCCESS('스케줄러 끝'))
