import psycopg2 as pg_db
import json

from psycopg2.extras import RealDictCursor
from babylon import ini_config


class DB:
    def __init__(self, filename, section='postgresql'):
        parser = ini_config.parse_ini_file(path=filename)
        if parser.has_section(section):
            params = parser.items(section)
            self.config = {param[0]: param[1] for param in params}
        else:
            raise Exception('Config not found for {0} in the file {1}'.format(section, filename))

    def add_event(self, event: dict):
        query = """INSERT INTO projects.events(id, "createdOn", "createdBy", type, stream, payload, about) 
        VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')"""

        with self.__get_db_connection() as db_connection:
            cursor = db_connection.cursor()
            cursor.execute(query % (event.get("id"), event.get("createdOn"), event.get("createdBy"), event.get("type"),
                                    event.get("stream"), json.dumps(event.get("payload")), event.get("about")))
            db_connection.commit()

    def get_all_events(self):
        query = "SELECT * FROM projects.events"

        with self.__get_db_connection() as db_connection:
            cursor = db_connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query)

            return cursor.fetchall()  # paginate this

    def get_event(self, event_id):
        found = list(filter((lambda event: event["id"] == event_id), self.get_all_events()))
        if not found:
            return None
        return found[0]

    def get_all_projects(self):
        query = "SELECT events.payload, events.about FROM projects.events WHERE events.type='create-project' " \
                "AND events.about NOT IN(SELECT events.about FROM projects.events WHERE events.type='delete-project')"

        with self.__get_db_connection() as db_connection:
            cursor = db_connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query)

            return cursor.fetchall()  # paginate this

    def get_project(self, project_id):
        found = list(filter((lambda project: project["payload"].get("id", project.get("about")) == project_id),
                            self.get_all_projects()))
        if not found:
            return None
        return found[0]

    def __get_db_connection(self):
        return pg_db.connect(host=self.config['host'],
                             database=self.config['database'],
                             port=self.config.get('port', 5432),
                             user=self.config['user'],
                             password=self.config['password'])
