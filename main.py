import os
import datetime
from todoist.api import TodoistAPI


def main():
    todoist_api_token = os.getenv("TODOIST_API_TOKEN")
    api = TodoistAPI(todoist_api_token)
    activity = api.activity.get()

    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=7)

    tasks = dict()
    for e in activity:
        done_time = datetime.datetime.strptime(e['event_date'], "%a %d %b %Y %H:%M:%S %z")
        if week_ago < done_time.date() < today:
            if e['event_type'] == "completed":
                if e['parent_project_id'] in tasks:
                    tasks[e['parent_project_id']].append(e)
                else:
                    tasks[e['parent_project_id']] = []
                    tasks[e['parent_project_id']].append(e)
    for k, p in tasks.items():
        print("* {}".format(api.projects.get(k)['project']['name']))
        dones = dict()
        for e in reversed(p):
            done_time = datetime.datetime.strptime(e['event_date'], "%a %d %b %Y %H:%M:%S %z")
            print("** <{}>{}".format(done_time.strftime('%Y-%m-%d %H:%M'), e['extra_data']['content']))
            taskId = e['object_id']
            for le in activity:
                if le['parent_item_id'] == taskId:
                    if not taskId in dones:
                        dones[taskId] = 1
                        print("\t- {}".format(le['extra_data']['content']))


if __name__ == "__main__":
    main()
