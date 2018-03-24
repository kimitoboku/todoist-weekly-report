import os
import datetime
from todoist.api import TodoistAPI


def main():
    todoist_api_token = os.getenv("TODOIST_API_TOKEN")
    api = TodoistAPI(todoist_api_token)
    activity = api.activity.get()

    tasks = dict()
    for e in activity:
        done_time = datetime.datetime.strptime(e['event_date'], "%a %d %b %Y %H:%M:%S %z")
        if e['event_type'] == "completed":
            if e['parent_project_id'] in tasks:
                tasks[e['parent_project_id']].append(e)
            else:
                tasks[e['parent_project_id']] = []
                tasks[e['parent_project_id']].append(e)
    for k, p in tasks.items():
        print("* {}".format(api.projects.get(k)['project']['name']))
        for e in p:
            print("** {}".format(e['extra_data']['content']))
            taskId = e['object_id']
            for le in activity:
                if le['parent_item_id'] == taskId:
                    print("\t- {}".format(le['extra_data']['content']))


if __name__ == "__main__":
    main()
