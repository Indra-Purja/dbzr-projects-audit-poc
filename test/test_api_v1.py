import pytest
import json

import os

from unittest import mock

from babylon.application import connexion
from babylon.config import ConfigWrapper, FileConfig


events = [
    {
        "id": "e520e6d5-5338-4a5c-9f87-8badf8eac9e5",
        "createdOn": "2019-09-20 09:23:54+01",
        "createdBy": "Alice",
        "type": "create-project",
        "stream": "projects",
        "about": "92b0a66d-d829-4cc8-acef-62930d08b0d6",
        "payload": {
            "id": "92b0a66d-d829-4cc8-acef-62930d08b0d6",
            "name": "Project One",
            "owner": "Alice"
        }
    },
    {
        "id": "5c789015-43e9-474e-bb36-be7e08ff6381",
        "createdOn": "2019-09-20 09:23:54+01",
        "createdBy": "Bob",
        "type": "create-project",
        "stream": "projects",
        "about": "3d96193d-ec39-439d-acf4-959930044428",
        "payload": {
            "id": "3d96193d-ec39-439d-acf4-959930044428",
            "name": "Project Two",
            "owner": "Bob"
        }
    }
]


@pytest.fixture(scope='module')
@mock.patch.dict(os.environ, {'SERVICE_NAME': 'dbzr-projects-audit'})
@mock.patch('dbzr_projects_audit.db.DB')
def test_client(test_db):
    config = connexion.config.Config(ConfigWrapper(FileConfig('.')),
                                     swagger_dir="../swagger/", api_spec='dbzr-projects-audit.yaml')
    flask_app = connexion.core.Application(config=config).flask_app
    flask_app.testing = True

    return flask_app.test_client()


@mock.patch('dbzr_projects_audit.db.DB.get_all_events')
def test_get_all_events_with_200_status(mock_events, test_client):
    mock_events.return_value = events
    response = test_client.get('/events')

    assert response.status_code == 200
    # assert b'"id": "100000"' in response.data


def test_get_an_event_with_200_status(test_client):
    response = test_client.get("/events/100000")

    assert response.status_code == 200

    content = json.loads(response.data)

    # assert content.get("_links").get("self").get("href") == "http://data-bazaar.com/v1/events/100000"
    # assert b'{"self": {"href": "http://data-bazaar.com/v1/events/100000"}}' \
    #        b'"id": "100000","name": "100000","createdOn": "","createdBy": "","type": "CreateProject",' \
    #        b'"stream": "","about": "Project-1","payload": {"id": "Project-1","name": "Project-One","owner": "Alice"}}' \
    #        in response.data
