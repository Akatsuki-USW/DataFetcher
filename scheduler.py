# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.triggers.cron import CronTrigger
# import threading
# import os
# import logging
#
# logger = logging.getLogger(__name__)
#
# def run_management_command(command_name):
#     os.system(f'python3 manage.py {command_name}')
#
# scheduler = BackgroundScheduler()
#
# jobs = [
#     {"function": "congestion_fetch", "minute": "20", "hour": "*"},
#     {"function": "daily_congestion_statistic", "minute": "30", "hour": "0"},
#     {"function": "weekly_congestion_statistic", "minute": "30", "hour": "0", "day_of_week": "mon"},
#     {"function": "sk_congestion_fetch", "minute": "18", "hour": "*"}
# ]
#
# for job in jobs:
#     trigger = CronTrigger(**{key: job.get(key) for key in ['minute', 'hour', 'day_of_week'] if job.get(key)})
#     scheduler.add_job(run_management_command, trigger, kwargs={"command_name": job["function"]})
#
# def run_scheduler():
#     scheduler.start()
#     try:
#         while True:
#             pass
#     except (KeyboardInterrupt, SystemExit):
#         scheduler.shutdown()
#
# if not scheduler.running:
#     thread = threading.Thread(target=run_scheduler)
#     thread.start()
#
#     logger.info('스케줄러 시작')
# else:
#     logger.info('스케줄러 실행 중...')
