#!/usr/bin/env python
#

import webapp2
import json
import cgi
from google.appengine.ext.webapp.util import run_wsgi_app
import MySQLdb
import os
import logging

def getDb():
    env = os.getenv('SERVER_SOFTWARE')
    if (env and env.startswith('Google App Engine/')):
      # Connecting from App Engine
      db = MySQLdb.connect(
        unix_socket='/cloudsql/newbase-testlukas:us',
        user='root',
        db = 'newbase')
    else:
      db = MySQLdb.connect(
        host = '173.194.228.163',
        port=3306,
        user = 'root',
        passwd = 'n3wb4s3L0L',
        db = 'newbase')
    return db

class MainHandler(webapp2.RequestHandler):
    def get(self):
        # for now direct SQL queries, in the future use django as ORM
        db = getDb();
        cursor = db.cursor()
        cursor.execute('SELECT * from projects')
        response = json.dumps(cursor.fetchall())

        logging.info('returning: ' + response)

        self.response.content_type = 'text/json'
        self.response.write(response)
        # other response stuff? https://webapp-improved.appspot.com/guide/response.html

    def post(self):
        name = self.request.get('name')
        logging.info('Inserting project named ' + name)

        db = getDb();
        cursor = db.cursor()
        cursor.execute('INSERT INTO projects (name) VALUES (%s)', [name])
        db.commit()
        db.close()

        self.redirect("/")

# webapp2: https://webapp-improved.appspot.com/index.html
app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)