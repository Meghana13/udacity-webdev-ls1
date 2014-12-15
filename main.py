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
import re

form="""
<form method="post">
	<b>Enter some text to ROT13:</b>
	<br>
	<textarea name="text" rows="8" cols="70">%(text)s</textarea>
	<br>
	<input type="submit">
</form>
"""

loginForm="""
<form method="post">
	<b>Signup</b>
	<br>
	
	<label>
		UserName
		<input type="text" name="username" value="%(username)s">
	</label>
	<div style="color: red">%(usernameError)s</div>
	
	<br>
	<label>
		Password
		<input type="password" name="password" value="%(password)s">
	</label>
	<div style="color: red">%(passwordError)s</div>
	<br>
	
	<label>
		Verify Password
		<input type="password" name="verify" value="%(verify)s">
	</label>
	<div style="color: red">%(verifyError)s</div>
	<br>

	<label>
		Email (optional)
		<input type="text" name="email" value="%(email)s">
	</label>
	<div style="color: red">%(emailError)s</div>
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

USER_RE=re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def validate_username(inputUserName):
	if USER_RE.match(inputUserName):
		return ""
	else:
		return "That's not a valid username" 

PASSWORD_RE=re.compile(r"^.{3,20}$")
def validate_password(inputPassword):
	if PASSWORD_RE.match(inputPassword):
		return ""
	else:
		return "That wasn't a valid password"


def validate_verify(inputPassword, inputVerify):
	if inputPassword==inputVerify:
		return ""
	else:
		return "Your passwords didn't match"

EMAIL_RE=re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def validate_email(inputEmail):
	if (inputEmail and not(EMAIL_RE.match(inputEmail))):
		return "That's not a valid email"
	else:
		return ""


class LoginHandler(webapp2.RequestHandler):
	def write_form(self, username="", password="", verify="", email="", usernameError="", passwordError="", verifyError="", emailError=""):
		self.response.out.write(loginForm %{"username":username, "password":password, "verify":verify, "email":email, "usernameError":usernameError, "passwordError":passwordError, "verifyError":verifyError, "emailError":emailError})
	
	def get(self):
		self.write_form()

	def post(self):

		input_username=self.request.get("username")
		input_password=self.request.get("password")
		input_verify=self.request.get("verify")
		input_email=self.request.get("email")


		username=validate_username(input_username)
		password=validate_password(input_password)
		verify=validate_verify(input_verify,input_password)
		email=validate_email(input_email)

		if (username=="" and password=="" and verify=="" and email==""):
			self.redirect("/welcome?username=%s" %input_username)
		
		else:
			self.write_form(input_username, "", "", input_email, username, password, verify, email)

class WelcomeHandler(webapp2.RequestHandler):
	def get(self):
		user=self.request.get("username")
		if (validate_username(user)==""):
			self.response.out.write("Welcome %s!" %user)
		else:
			self.redirect('/unit2/signup')
	
app = webapp2.WSGIApplication([
    ('/unit2/rot13', MainHandler),
    ('/unit2/signup',LoginHandler),
    ('/welcome', WelcomeHandler)
    ], debug=True)
