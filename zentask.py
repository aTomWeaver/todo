import argparse
import json
from datetime import datetime

current_tasks_dict = json.load(open('./current.json', 'r'))

# helpers


def get_int_key_list(task_dict: dict):
    return [int(key) for key in task_dict.keys()]


def reindex(dict):
    '''If highest task index is greater than the amount of tasks,
    reindex tasks sequentially so that indexes don't continuously increase.
    '''
    # get keys as list of ints
    keys = get_int_key_list(dict)

    # reindex
    if int(max(keys)) > len(keys):
        i = 1
        for key in keys:
            dict[i] = dict.pop(str(key))
            i += 1

    # overwrite
    with open('current.json', 'w', encoding='utf-8') as current:
        json.dump(dict, current)


def get_max_value_length(value):
    max_value_length = 0

    for key in current_tasks_dict.keys():
        value_length = len(current_tasks_dict[key][value])
        if value_length > max_value_length:
            max_value_length = value_length
    return max_value_length


# create
def add_task(new_task: dict):
    '''Saves a new task to current.json from given dict of
    {title, priority, context, project}.
    '''
    # copy and re-index current_task_dict
    current_tasks_copy = current_tasks_dict.copy()
    reindex(current_tasks_copy)
    keys = get_int_key_list(current_tasks_copy)
    new_task_index = max(keys) + 1

    current_tasks_copy[str(new_task_index)] = new_task
    with open('current.json', 'w', encoding='utf-8') as current:
        json.dump(current_tasks_copy, current)
    pass

# read


def list_current_tasks():
    current_tasks_dict = json.load(open('./current.json', 'r'))
    reindex(current_tasks_dict)
    max_title_lenth = get_max_value_length('title') + 1
    max_context_length = get_max_value_length('context') + 1

    for key in current_tasks_dict.keys():
        task = current_tasks_dict[key]

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
    "title": "check if work",
    "priority": "a",
    "context": "",
    "project": "get working"
})
list_current_tasks()
