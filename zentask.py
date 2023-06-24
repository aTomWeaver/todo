import argparse
import json
from datetime import datetime


# create
def add_task():
  task = json.dumps({"title": "testing", "priority": "c", "context": "home"}, indent=2)
  print(task)
  pass

# read
def list_current_tasks():
  pass

def list_archived_tasks():
  pass

# delete
def delete_task(task):
  pass


def complete_task(task):
  # remove task from current
  # append task to archive with completion date
  timestamp = datetime.now().strftime('%Y/%m/%d %H:%M')
  print(f'\nTask completed: {task}\nCompletion Date: {timestamp}')

add_task()

