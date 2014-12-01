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
import webapp2
import cgi

form="""
<form method="post">
	<b>Enter some text to ROT13:</b>
	<br>
	<textarea name="text" rows="8" cols="70">%(text)s</textarea>
	<br>
	<input type="submit">
</form>
"""

def encode_rot13(inputString):
	encryptedString=""
	encryptedCharacter=""

	for character in inputString:
		if character.isalpha():

			offsetValue=0
			if character.islower():
				offsetValue=ord('a')
			else:
				offsetValue=ord('A')

			encryptedCharacter=chr((((ord(character)-offsetValue)+13)%26)+offsetValue)
	            
		else:
			encryptedCharacter=character
		
		encryptedString+=encryptedCharacter
	return encryptedString

class MainHandler(webapp2.RequestHandler):
    def write_form(self,text=""):
	    if text:
		    text=encode_rot13(text)
		    text=cgi.escape(text, quote=True)
	    self.response.out.write(form %{"text":text})

    def get(self):
	    self.write_form()

    def post(self):
	    text=self.request.get("text")
	    self.write_form(text)

	
app = webapp2.WSGIApplication([
    ('/unit2/rot13', MainHandler)
], debug=True)
