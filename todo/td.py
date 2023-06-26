from argparse import ArgumentParser
import json
from datetime import datetime
import os
from termcolor import colored


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
    try:
        if int(max(keys)) > len(keys):
            i = 1
            for key in keys:
                dict[i] = dict.pop(str(key))
                i += 1
    except:
        print('no items in list')
        return dict
    return dict


def get_max_value_length(value, task_dict):
    '''returns the max length of a given value in a given task_dict'''
    max_value_length = 0

    for key in task_dict.keys():
        value_length = len(task_dict[key][value])
        if value_length > max_value_length:
            max_value_length = value_length
    return max_value_length


def filter_dict(dict, filter_key, filter_value):
    filtered_dict = {}
    for key, inner_dict in dict.items():
        if inner_dict[filter_key] == filter_value:
            filtered_dict[key] = inner_dict
    return filtered_dict


def clear_and_list(dict):
    os.system('clear')
    CLI.print_tasks(dict)


# classes


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


class TaskList:
    def __init__(self):
        self.current_tasks_dict = json.load(
            open('/home/tom/code/python/td/todo/current.json', 'r'))
        self.current_json_path = '/home/tom/code/python/td/todo/current.json'
        self.archive_json_path = '/home/tom/code/python/td/todo/archive.json'

    def refresh_current(self):
        self.current_tasks_dict = json.load(open(self.current_json_path, 'r'))

    def write_to_json_file(self, dict, destination):
        with open(destination, 'w', encoding='utf-8') as destination:
            json.dump(dict, destination)

    def archive_task(self, task):
        '''appends task dict to archive.json'''
        # this is inefficient. maybe just append to a text file?
        archive_json_copy = json.load(open(self.archive_json_path, 'r'))

        keys = get_int_key_list(archive_json_copy)
        if not keys:
            index = 1
        else:
            index = max(keys) + 1

        archive_json_copy[index] = task
        self.write_to_json_file(archive_json_copy, self.archive_json_path)

    def add_task(self, title, priority, context, project):
        '''Saves a new task to current.json from passed props'''
        # copy and re-index current_task_dict
        current_tasks_copy = self.current_tasks_dict.copy()
        current_tasks_copy = reindex(current_tasks_copy)
        current_tasks_copy_keys = get_int_key_list(current_tasks_copy)
        if not current_tasks_copy_keys:
            new_task_index = 1
        else:
            new_task_index = max(current_tasks_copy_keys) + 1
        # append new task to current task copy dict
        current_tasks_copy[str(new_task_index)] = Task(
            title, priority, context, project).get_dict()
        # write current task copy to current.json
        self.write_to_json_file(current_tasks_copy, self.current_json_path)

    def pop_task(self, task_index):
        self.refresh_current()

        current_tasks_copy = self.current_tasks_dict.copy()
        if not task_index in current_tasks_copy:
            return None
        # pop and catch task from current_tasks_copy
        removed = current_tasks_copy.pop(task_index)
        current_tasks_copy = reindex(current_tasks_copy)
        # write modified copy to json
        self.write_to_json_file(current_tasks_copy, self.current_json_path)
        return removed

    def complete_task(self, task_index):
        '''moves task from current to archive with a completion date'''

        # edit this to accept n number of task indexes

        try:
            task = self.pop_task(task_index)
            timestamp = datetime.now().strftime('%Y/%m/%d %H:%M')
            task['completed'] = timestamp

            self.archive_task(task)

            print(
                f'Task completed: {task["title"]}\nCompletion Date: {timestamp}\n')
        except:
            print(f'No task with index {task_index}\n')
            return None


current_tasks = TaskList()


####################################
###### COMMAND LINE INTERFACE ######
####################################

# term colors

class c:
    def index(text):
        return colored(text, 'yellow', attrs=['dark'])

    def p_a(text):
        return colored(text, 'red')

    def p_b(text):
        return colored(text, 'yellow')

    def p_c(text):
        return colored(text, 'green')

    def p_d(text):
        return colored(text, 'magenta')

    def context(text):
        return colored(text, 'light_green')

    def project(text):
        return colored(text, 'light_yellow')

    def get_priority_color(priority):
        if priority == 'a':
            return c.p_a
        elif priority == 'b':
            return c.p_b
        elif priority == 'c':
            return c.p_c
        else:
            return c.p_d


class CLI:
    def print_tasks(dict):
        '''prints out tasks to the command line'''

        current_tasks.refresh_current()
        current_tasks.current_tasks_dict = reindex(
            current_tasks.current_tasks_dict)

        max_title_length = get_max_value_length(
            'title', dict) + 1
        max_context_length = get_max_value_length(
            'context', dict) + 1
        max_project_length = get_max_value_length('project', dict)

        print('--todo' + ('-' * (max_title_length +
              max_context_length + max_project_length)))

        for key in dict.keys():
            task = dict[key]
            title_right_pad = (max_title_length - len(task["title"])) * ' '
            context_right_pad = (max_context_length -
                                 len(task["context"])) * ' '
            priority_color = c.get_priority_color(task['priority'])
            formatted_priority = priority_color(f'({task["priority"]})')
            formatted_context = c.context(f'@{task["context"]}')
            formatted_project = c.project(f'+{task["project"]}')

            output = f'{c.index(key)} {formatted_priority} {task["title"]}{title_right_pad}'

            if task["context"]:
                output += f'{formatted_context}{context_right_pad}'
            else:
                output += f'{context_right_pad} '
            if task["project"]:
                output += formatted_project

            print(output)


parser = ArgumentParser(description='Simple CLI todo app')

# the first argument will be for the 'command'(l, a, c, d)
subparsers = parser.add_subparsers(dest="command")

# 'list' command parser
list_parser = subparsers.add_parser('l', help='list current tasks')
list_parser.add_argument('-pt', '--priority', nargs='?',
                         help='list only tasks from the given priority')
list_parser.add_argument('-c', '--context', nargs='?',
                         help='list only tasks from the given context')
list_parser.add_argument('-p', '--project', nargs='?',
                         help='list only tasks from the given project')

# 'add' command parser
add_task_parser = subparsers.add_parser(
    'a', help='add a task via `a <task title> <priority> (context) (project)`')
add_task_parser.add_argument('title', nargs='?', help='the name of the task')
add_task_parser.add_argument(
    'priority', nargs='?', help='the priority of the task')
add_task_parser.add_argument('-c', '--context', nargs='?',
                             help='the context in which the task should be performed (e.g. home, office, etc.)')
add_task_parser.add_argument('-p', '--project', nargs='?',
                             help='(optional) the project that the task is for')

# 'complete' command parser
complete_task_parser = subparsers.add_parser(
    'c', help='complete a task via `c <task index>`')
complete_task_parser.add_argument(
    'task_index', nargs='?', help='the index of the task to be completed')

# 'delete' command parser
delete_task_parser = subparsers.add_parser(
    'd', help='delete a task via `d <task index>`')
delete_task_parser.add_argument(
    'task_index', nargs='?', help='the index of the task to be deleted')

args = parser.parse_args()


def main():
    # Try to make this section less disgusting & more DRY
    if args.command == 'l':
        if args.priority:
            filtered_dict = filter_dict(
                current_tasks.current_tasks_dict, 'priority', args.priority)
            clear_and_list(filtered_dict)
        elif args.context:
            filtered_dict = filter_dict(
                current_tasks.current_tasks_dict, 'context', args.context)
            clear_and_list(filtered_dict)
        elif args.project:
            filtered_dict = filter_dict(
                current_tasks.current_tasks_dict, 'project', args.project)
            clear_and_list(filtered_dict)
        else:
            current_tasks.refresh_current()
            clear_and_list(current_tasks.current_tasks_dict)
    elif args.command == 'a':
        if not args.title:
            parser.error("The 'title' argument is required for adding a task")
        else:
            if not args.priority:
                parser.error(
                    "The 'priority' argument is required for adding a task")
            else:
                if args.context:
                    context = args.context
                else:
                    context = ''
                if args.project:
                    project = args.project
                else:
                    project = ''
                current_tasks.add_task(
                    args.title, args.priority, context, project)
                current_tasks.refresh_current()
                clear_and_list(current_tasks.current_tasks_dict)
    elif args.command == 'c':
        if not args.task_index:
            parser.error(
                "The 'task index' argument is required for completing a task")
        else:
            current_tasks.complete_task(args.task_index)
            current_tasks.refresh_current()
            clear_and_list(current_tasks.current_tasks_dict)
    elif args.command == 'd':
        if not args.task_index:
            parser.error(
                "The 'task index' argument is required for completing a task")
        else:
            current_tasks.pop_task(args.task_index)
            current_tasks.refresh_current()
            clear_and_list(current_tasks.current_tasks_dict)
