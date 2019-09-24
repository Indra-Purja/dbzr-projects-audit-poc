import uuid
import json
import connexion
from datetime import datetime

from dbzr_projects_audit.db import DB

not_found_error_message = "Not Found"

db = DB("dbzr_projects_audit/config.ini")


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

    return __event_response_content("{}/{}".format(connexion.request.url, event.get("id")), event), 201


def get_events():
    all_events = []
    events = db.get_all_events()
    for event in events:
        all_events.append(__event_response_content("{}/{}".format(connexion.request.url, event.get("id")), event))
    return {**__self_ref_and_name(connexion.request.url, "all-events"), "events": all_events}, 200


def get_event(event_id):
    event = db.get_event(event_id)
    if event is None:
        return not_found_error_message, 404

    return __event_response_content(connexion.request.url, event), 200


def get_projects():
    all_projects = []
    projects = db.get_all_projects()
    for project in projects:
        all_projects.append(__project_response_content(project, True))
    return {**__self_ref_and_name(connexion.request.url, "all-projects"), "projects": all_projects}, 200


def get_project(project_id):
    project = db.get_project(project_id)
    if project is None:
        return not_found_error_message, 404

    return __project_response_content(project, False), 200


def __event_response_content(self_url, event):
    return {**__self_ref_and_name(self_url, "event-{}".format(event.get("id"))), **event}


def __project_response_content(project: dict, construct_self_url: bool):
    payload = project.get("payload")
    project_id = payload.get("id", project.get("about"))
    project_name = project.get("name", "project-{}".format(project_id))
    self_url = __project_self_url(construct_self_url, project_id)

    return {**__self_ref_and_name(self_url, project_name), "id": project_id,
            **payload}


def __project_self_url(construct_self_url: bool, project_id: str):
    if construct_self_url:
        return "{}/{}".format(connexion.request.url, project_id)
    else:
        return connexion.request.url


def __self_ref_and_name(self_url, name) -> dict:
    return {"_links": {"self": {"href": self_url}}, "name": name}
