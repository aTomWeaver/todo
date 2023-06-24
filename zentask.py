import argparse
import json
from datetime import datetime
from pprint import pprint

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
    return dict


def get_max_value_length(value, task_dict):
    '''returns the max length of a given value in a given task_dict'''
    max_value_length = 0

    for key in task_dict.keys():
        value_length = len(task_dict[key][value])
        if value_length > max_value_length:
            max_value_length = value_length
    return max_value_length

# classes


class TaskList:
    def __init__(self):
        self.current_tasks_dict = json.load(open('./current.json', 'r'))

    def refresh_current(self):
        self.current_tasks_dict = json.load(open('./current.json', 'r'))

    def write_to_current_json(self, file_to_write):
        with open('current.json', 'w', encoding='utf-8') as current:
            json.dump(file_to_write, current)

    def archive_task(self, task):
        '''appends task to archive.json'''
        pass

    def add_task(self, title, priority, context, project):
        '''Saves a new task to current.json from passed props'''
        # copy and re-index current_task_dict
        current_tasks_copy = self.current_tasks_dict.copy()
        current_tasks_copy = reindex(current_tasks_copy)
        keys = get_int_key_list(current_tasks_copy)
        new_task_index = max(keys) + 1

        current_tasks_copy[str(new_task_index)] = Task(
            title, priority, context, project).get_dict()
        self.write_to_current_json(current_tasks_copy)

    def delete_task(self, task):
        pass

    def list_current_tasks(self):
        '''prints out tasks to the command line'''
        self.refresh_current()
        self.current_tasks_dict = reindex(self.current_tasks_dict)
        max_title_lenth = get_max_value_length(
            'title', self.current_tasks_dict) + 1
        max_context_length = get_max_value_length(
            'context', self.current_tasks_dict) + 1

        for key in self.current_tasks_dict.keys():
            task = self.current_tasks_dict[key]

            title_right_pad = (max_title_lenth - len(task["title"])) * ' '
            context_right_pad = (max_context_length -
                                 len(task["context"])) * ' '

            print_line = f'{key} ({task["priority"]}) {task["title"]}{title_right_pad}'

            if task["context"]:
                print_line += f'@{task["context"]}{context_right_pad}'
            else:
                print_line += f'{context_right_pad} '

            if task["project"]:
                print_line += f'+{task["project"]}'

            print(print_line)

    def complete_task(self, task):
        '''moves task from current to archive with a completion date'''

        timestamp = datetime.now().strftime('%Y/%m/%d %H:%M')
        task['completed'] = timestamp

        self.archive_task(task)
        self.delete_task(task)

        print(
            f'\nTask completed: {task["title"]}\nCompletion Date: {timestamp}')
        print(f'\n{task}')
    pass


class Task:
    def __init__(self, title, priority="u", context="", project=""):
        self.title = title
        self.priority = priority
        self.context = context
        self.project = project

    def get_dict(self):
        return {
            "title": self.title,
            "priority": self.priority,
            "context": self.context,
            "project": self.project
        }


current_tasks = TaskList()
current_tasks.list_current_tasks()
current_tasks.print_task_list()
