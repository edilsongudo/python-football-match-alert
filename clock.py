from apscheduler.schedulers.blocking import BlockingScheduler

from football_alert import main

sched = BlockingScheduler()
sched.add_job(main, 'interval', minutes=60)
sched.start()
