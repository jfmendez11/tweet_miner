from crontab import CronTab
import os
import schedule
import time

def job():
  os.system("python3 main.py")

if __name__ == "__main__":
  print("Initial load")
  job()
  
  print("Starting cron job")
  schedule.every().day.at("00:00").do(job)
  
  while True:
    schedule.run_pending()
    time.sleep(1)
