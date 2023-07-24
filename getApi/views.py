from django.shortcuts import render
from apscheduler.schedulers.background import BackgroundScheduler


scheduler = BackgroundScheduler()
def get_scheduler_status():

    jobs = scheduler.get_jobs()
    return jobs

def index(request):
    return render(request, "main/mainpage.html")

def scheduler_status(request):
    jobs = get_scheduler_status()
    return render(request, 'api/scheduler_status.html', {'jobs': jobs})
