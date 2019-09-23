import uuid
import json
from datetime import datetime

from dbzr_projects_audit.db import DB

not_found_error_message = "Not Found"

db = DB("dbzr_projects_audit/config.ini")
host_url = "http://localhost:8000/dbzr-projects-audit/v1"


def post_event(body):
    event = dict()

    event['id'] = str(uuid.uuid4())
    event['createdOn'] = str(datetime.utcnow())
    event['createdBy'] = body.get('createdBy')
    event['type'] = body.get('type')
    event['stream'] = body.get('stream')
    event['payload'] = json.loads(body.get('payload', "{}"))
    event['about'] = event.get('payload').get('id', str(uuid.uuid4()))

    db.add_event(event)

    return __event_response_content(event), 201


def get_events():
    all_events = []
    events = db.get_all_events()
    for event in events:
        all_events.append(__event_response_content(event))
    return {**__self_ref_and_name("{}/{}".format(host_url, "events"), "all-events"), "events": all_events}, 200


def get_event(event_id):
    event = db.get_event(event_id)
    if event is None:
        return not_found_error_message, 404

    return __event_response_content(event), 200


def get_projects():
    all_projects = []
    projects = db.get_all_projects()
    for project in projects:
        all_projects.append(__project_response_content(project))
    return {**__self_ref_and_name("{}/{}".format(host_url, "projects"), "all-projects"), "projects": all_projects}, 200


def get_project(project_id):
    project = db.get_project(project_id)
    if project is None:
        return not_found_error_message, 404

    return __project_response_content(project), 200


def __event_response_content(event):
    return {**__self_ref_and_name("{}/{}/{}".format(host_url, "events", event.get("id")),
                                  "event-{}".format(event.get("id"))), **event}


def __project_response_content(project):
    payload = project.get("payload")
    project_id = payload.get("id", project.get("about"))
    project_name = project.get("name", "project-{}".format(project_id))
    return {**__self_ref_and_name("{}/{}/{}".format(host_url, "projects", project_id), project_name), "id": project_id,
            **payload}


def __self_ref_and_name(ref_url, name) -> dict:
    return {"_links": {"self": {"href": ref_url}}, "name": name}
