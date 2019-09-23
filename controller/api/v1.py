import uuid
import json
from datetime import datetime
from datetime import timezone

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

    return event, 201


def get_events():
    return db.get_all_events(), 200


def get_event(event_id):
    event = db.get_event(event_id)
    if event is None:
        return not_found_error_message, 404

    return event, 200


def get_projects():
    return db.get_all_projects(), 200


def get_project(project_id):
    project = db.get_project(project_id)
    if project is None:
        return not_found_error_message, 404

    return project, 200
