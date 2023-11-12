from datetime import datetime


def current_time_to_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def create_task_strings_for_rows(data):
    ready, doing, done = "", "", ""

    for id, task in data.items():
        task_id = f" [[cyan]{id}[/]]\t"
        task_tag = f'([orange3]{task.get("Tag")}[/])'
        task_title = f' [royal_blue1]{task["Title"]}[/]\n'
        task_total_str = task_id + task_tag + task_title
        if task["Status"] == "ready":
            ready += task_total_str
        if task["Status"] == "doing":
            doing += task_total_str
        if task["Status"] == "done":
            done += task_total_str

    return ready, doing, done
