#!/usr/bin/env python
#

import webapp2
import json

class MainHandler(webapp2.RequestHandler):
    def get(self):
        stuff = ['foo', {'bar': ('baz', None, 1.0, 2)}]
        self.response.content_type = 'text/json'
        self.response.write(json.dumps(stuff))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
