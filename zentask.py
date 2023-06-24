import argparse
import json
from datetime import datetime

tasks = json.load(open('./current.json', 'r'))


def refresh_tasks():
    tasks = json.load(open('./current.json', 'r'))


refresh_tasks()
# helpers


def reindex(dict):
    keys = [int(key) for key in dict.keys()]

    if int(max(keys)) > len(keys):
        i = 1
        for key in keys:
            dict[i] = dict.pop(str(key))
            i += 1
    with open('current.json', 'w', encoding='utf-8') as current:
        json.dump(dict, current)


def get_max_value_length(value):
    max_value_length = 0

    for key in tasks.keys():
        value_length = len(tasks[key][value])
        if value_length > max_value_length:
            max_value_length = value_length
    return max_value_length


# create
def add_task(new_task: dict):
    '''accepts dict of title, priority, context, project'''
    task_buffer = tasks.copy()
    reindex(task_buffer)
    keys = [int(key) for key in task_buffer.keys()]
    new_task_index = max(keys) + 1

    task_buffer[str(new_task_index)] = new_task
    with open('current.json', 'w', encoding='utf-8') as current:
        json.dump(task_buffer, current)
    pass

# read


def list_current_tasks():
    tasks = json.load(open('./current.json', 'r'))
    reindex(tasks)
    max_title_lenth = get_max_value_length('title') + 1
    max_context_length = get_max_value_length('context') + 1

    for key in tasks.keys():
        task = tasks[key]

        title_right_pad = (max_title_lenth - len(task["title"])) * ' '
        context_right_pad = (max_context_length - len(task["context"])) * ' '

        line = f'{key} ({task["priority"]}) {task["title"]}{title_right_pad}'
        if task["context"]:
            line += f'@{task["context"]}{context_right_pad}'
        else:
            line += f'{context_right_pad} '
        if task["project"]:
            line += f'+{task["project"]}'
        print(line)
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


add_task({
    "title": "go to the movies",
    "priority": "d",
    "context": "outside",
    "project": ""
})

list_current_tasks()
