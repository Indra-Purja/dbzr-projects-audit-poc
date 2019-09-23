import dbzr_projects_audit.db as db
import json


def test_get_all_events():
    assert json.loads(db.get_all_events()) == db.events


def test_get_a_event():
    expected = {
            "_links": {
                "self": {
                    "href": "http://data-bazaar.com/v1/events/100000"
                }
            },
            "id": "100000",
            "name": "100000",
            "createdOn": "",
            "createdBy": "",
            "type": "CreateProject",
            "stream": "",
            "about": "project-1",
            "payload": {
                "id": "project-1",
                "name": "Project-One",
                "owner": "Alice"
            }
        }

    assert db.get_event("100000") == expected


def test_get_all_projects():
    assert json.loads(db.get_all_projects()) == db.projects


def test_get_a_project():
    expected = {
            "_links": {
                "self": {
                    "href": "http://data-bazaar.com/v1/projects/project-1"
                }
            },
            "id": "project-1",
            "name": "Project One",
            "createdOn": "",
            "owner": "Alice"
        }

    assert db.get_project("project-1") == expected
