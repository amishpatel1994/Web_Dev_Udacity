import webapp2

form = """
<html>
	<head>
		<title>Rot_13 Text Converter</title>
	</head>

	<body>
		<h1>Rot_13 Converter</h1>
		<form method="post">
			<textarea name="text" style="height:250px; width:500px">%(info)s</textarea> <br>
			<input type="submit" value="Submit">
		</form>
	</body>
</html>

"""


class MainPage(webapp2.RequestHandler):

	def escape_html(self,s):
		for (i,o) in ( ('&','&amp;'),('>','&gt;'), ('<','&lt;'), ('"','&quot;')):
			s = s.replace(i,o)
		return s

	def write_form(self,information=""):
		self.response.out.write(form % {"info": information})

	def change_to_rot_13(self,st):
		g = ""
		count = 0
		for b in st:
			#return ord('a')
			if (b.isalpha()):
				if (b.isupper()):
					g += str(chr(((ord(b.lower()) + 13 - 97) % 26)+97).upper())
				else:
					g += str(chr(((ord(b) + 13 - 97) % 26)+97))
			else:
				g += str(b)
			count = count + 1
		return g

	def change_rot_13_to_norm(self,st):
		g = ""
		count = 0
		for b in st:
			#return ord('a')
			if (b.isalpha()):
				if (b.isupper()):
					g += str(chr(((ord(b.lower()) - 13 - 97) % 26)+97).upper())
				else:
					g += str(chr(((ord(b) - 13 - 97) % 26)+97))
			else:
				g += str(b)
			count = count + 1
		return g

	def post(self):
		text = self.request.get('text')
		counter = 0
		if (counter % 2 == 0):
			text = self.change_to_rot_13(text)
			counter = counter + 1
		else:
			text = self.change_rot_13_to_norm(text)
			counter = counter + 1
		self.write_form(self.escape_html(text))

	def get(self):
		self.write_form()



application = webapp2.WSGIApplication([("/",MainPage)],debug=True)
