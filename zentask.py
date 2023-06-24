import argparse
import json
from datetime import datetime

tasks = json.load(open('./current.json', 'r'))

# helpers


def reindex_tasks():
    keys = [int(key) for key in tasks.keys()]

    if int(max(keys)) > len(keys):
        i = 1
        for key in keys:
            tasks[i] = tasks.pop(str(key))
            i += 1
    else:
        print('already properly indexed')
    with open('current.json', 'w', encoding='utf-8') as current:
        json.dump(tasks, current)


def get_max_value_length(value):
    max_value_length = 0

    for key in tasks.keys():
        value_length = len(tasks[key][value])
        if value_length > max_value_length:
            max_value_length = value_length
    return max_value_length


# create
def add_task():
    task = json.dumps({"title": "testing", "priority": "c",
                      "context": "home"}, indent=2)
    print(task)
    reindex_tasks()
    pass

# read


def list_current_tasks():
    reindex_tasks()
    max_title_lenth = get_max_value_length('title')
    max_context_length = get_max_value_length('context')

    for key in tasks.keys():
        title = tasks[key]["title"]
        priority = tasks[key]["priority"]
        context = tasks[key]["context"]
        project = tasks[key]["project"]
        title_right_pad = (max_title_lenth - len(title)) * ' '
        context_right_pad = (max_context_length - len(context)) * ' '

        print(
            f'{key} ({priority}) {title} {title_right_pad}@{context}{context_right_pad} +{project}')
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


# add_task()
list_current_tasks()
