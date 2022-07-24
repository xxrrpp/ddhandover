from datetime import datetime
import time
import requests
import os

# import dget.info as info
from apscheduler.schedulers.blocking import BlockingScheduler


def upd():
    s = requests.Session()
    r = s.get("xxxx/upda/")
    print(r, r.text)
    time.sleep(1)
    r = s.get("xxxx/updp/")
    print(r, r.text)
    time.sleep(1)
    r = s.get("xxxx/updc/")
    print(r, r.text)
    time.sleep(1)
    r = s.get("xxxx/updb/")
    print(r, r.text)
    time.sleep(2)
    r = s.get("xxxx/save/")
    print(r)
    del s
    print("update chain >>> done")


def tick():
    global timestarted
    try:
        timestarted
    except:
        timestarted = time.time()
    print("running: {} min".format(round((time.time() - timestarted) / 60, 2)))
    # print('Tick! The time is: %s' % datetime.now())


def ping():
    print(requests.get("xxxxx.com/").text)


if __name__ == "__main__":
    print("clock has started: %s" % datetime.now())
    upd()
    scheduler = BlockingScheduler()
    scheduler.add_job(tick, "interval", minutes=10)
    scheduler.add_job(upd, "interval", minutes=60)
    scheduler.add_job(ping, "interval", minutes=25)
    # print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
