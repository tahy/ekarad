import cherrypy
import os
import sqlite3
from time import time

DB_STRING = "/opt/db/my.db"

def setup_database():
    """
    Create the `statistics` table in the database
    on server startup
    """

    items = [
        ( str(time()), 'Радищева 10', '100'),
        ( str(time()), 'Ленина 66', '45'),
        ( str(time()), 'Космонавтов 41', '11'),
        ( str(time()), 'Куйбышева 18', '10'),
        ( str(time()), 'Уральская 45', '12'),
        ( str(time()), 'Сибирский тракт 3', '7'),
    ]

    with sqlite3.connect(DB_STRING) as con:
        con.execute("CREATE TABLE statistics (created, location, value)")
        con.executemany("INSERT INTO statistics VALUES (?, ?, ?)", items)
        con.commit()

def cleanup_database():
    """
    Destroy the `user_string` table from the database
    on server shutdown.
    """
    with sqlite3.connect(DB_STRING) as con:
        con.execute("DROP TABLE statistics")

class Root:
    @cherrypy.expose
    def index(self):

        with sqlite3.connect(DB_STRING) as c:
            r = c.execute("SELECT created, location, value FROM statistics")
        return {'items': r.fetchall()}

if __name__ == '__main__':
    # Register the Mako plugin
    from makoplugin import MakoTemplatePlugin
    MakoTemplatePlugin(cherrypy.engine, base_dir=os.getcwd()).subscribe()

    # Register the Mako tool
    from makotool import MakoTool
    cherrypy.tools.template = MakoTool()

    conf = {
        '/': {
            'tools.template.on': True,
            'tools.template.template': 'tmpl/index.html',
            'tools.encode.on': False,

            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': '/opt/src/static'
        }
    }

    cherrypy.engine.subscribe('start', setup_database)
    cherrypy.engine.subscribe('stop', cleanup_database)

    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.quickstart(Root(), '', conf)