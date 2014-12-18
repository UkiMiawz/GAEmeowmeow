#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import logging
import os
from google.appengine.ext import ndb

import webapp2
import jinja2

from model import MovieQuote

jinja_env = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
	autoescape = True)

#generic key to serve as the parent
PARENT_KEY = ndb.Key("Entity", "moviequote_root")

class MainHandler(webapp2.RequestHandler):
    def get(self):

    	#create query fetch
		moviequotes_query = MovieQuote.query(ancestor=PARENT_KEY).order(-MovieQuote.last_touch_date_time)
		template = jinja_env.get_template("templates/moviequotes.html")
		self.response.write(template.render({"moviequotes_query" : moviequotes_query}))
        #self.response.write('Hello world! Hurrr Duurrrr Durrrr Hurrrr')

class AddQuoteAction(webapp2.RequestHandler):
	def post(self):

		quote = self.request.get("quote")
		movie = self.request.get("movie")
		
		new_moviequote = MovieQuote(parent=PARENT_KEY, quote=self.request.get("quote"), movie=self.request.get("movie"))
		new_moviequote.put()

		self.redirect(self.request.referer)
		
		logging.info("TODO: Add quote " + quote + " from movie " + movie)
		#self.response.write("TODO: Add quote " + quote + " from movie " + movie)

app = webapp2.WSGIApplication([
    ("/", MainHandler),
    ("/addquote", AddQuoteAction)
], debug=True)
