import os
import jinja2
import webapp2
import re
from google.appengine.ext import db
import hmac
import random
import hashlib
from string import letters

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape=True)

SECRET = "UGHLA22saDASD32423sdsdsAS"

def make_salt(length = 5):
	return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(key,pw,salt=None):
	if not salt:
		salt = make_salt()
	hash_val = hashlib.sha256(key + pw + salt).hexdigest()
	return '%s,%s' % (salt,hash_val)

def verify_pw(key,pw,hash_val):
	salt = hash_val.split(',')[0]
	return hash_val == make_pw_hash(key,pw,salt)
# entity class to store the blog entries
class Blogs(db.Model):
	subject = db.StringProperty(required=True)
	content = db.TextProperty(required=True)
	created = db.DateTimeProperty(auto_now_add=True)
	dateCreated = db.DateProperty(auto_now_add=True)


# common handler with helper functions to render html templates with the contents
class Handler(webapp2.RequestHandler):
	def write(self,*k,**a):
		self.response.out.write(*k,**a)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self,template,**kw):
		self.write(self.render_str(template, **kw))

	def hash_str(self,s):
		return hmac.new(SECRET,s).hexdigest()

	def make_secure_val(self,s):
		return "%s|%s" % (s,self.hash_str(s))

	def check_secure_val(self,h):
		val = h.split('|')[0]
		if h == self.make_secure_val(val):
			return val

	#def users_key(group = 'default'):
		#return db.Key.from_path('users',group)

	def set_cookie(self,key,value):
			cookie = self.make_secure_val(value)
			self.response.headers.add_header('Set-Cookie',
				'%s=%s; Path=/' % (key,cookie))

	def read_cookie(self,key):
		cookie = self.request.cookies.get(key)
		return cookie and self.check_secure_val(cookie)

	def login(self,user):
		return self.set_cookie('user_id',str(user.key().id()))

	def logout(self):
		self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

	def init(self,*a,**kw):
		webapp2.RequestHandler.initialize(self,*a,**kw)
		uid = self.read_cookie('user_id')
		self.user = uid and User.by_id(int(uid))

class User(db.Model,Handler):
	name = db.StringProperty(required=True)
	password_hash = db.StringProperty(required=True)
	email = db.StringProperty()

	@classmethod
	def by_id(clas,uid):
		return User.get_by_id(uid)

	@classmethod
	def by_name(clas,name):
		user = User.all().filter('name =', name).get()
		return user

	@classmethod
	def register(clas,name,pw,email=None):
		salt = ''.join(random.choice(letters) for x in xrange(5))
		hash_val = hashlib.sha256(name + pw + salt).hexdigest()
		return User(
			name = name,
			password_hash = '%s,%s' % (salt,hash_val),
			email=email)

	@classmethod
	def login(cls,name,pw):
		user = cls.by_name(name)
		if user and verify_pw(name,pw,user.password_hash):
			return user

# main page where the 10 recent entries are listed
class MainPage(Handler):
	def get(self):
		blogs = db.GqlQuery("SELECT * from Blogs ORDER BY created desc")
		self.render("home.html",blogs=blogs)

# page where you enter new blog entries
class NewBlog(Handler):
	def render_entry(self,error="",subject="",content=""):
		self.render("entry.html",error=error,content=content,subject=subject)

	def get(self):
		self.render_entry()

	def post(self):
		subject = self.request.get('subject')
		content = self.request.get('content')

		if subject and content:
			blg = Blogs(subject=subject,content=content)
			blg.put()
			obj_id = blg.key().id()
			self.redirect("/%s" % obj_id)
		else:
			self.render_entry(error="Both subject and content must be filled!",subject=subject,content=content)

# class for permalinks(to show a single blog entry on a page)
class BlogHandler(Handler):
    def get(self, product_id):
    	blog_post = Blogs.get_by_id(int(product_id),parent=None)
    	self.render("blog.html",entry=blog_post)
        #self.response.write('This is the ProductHandler. '
         #   'The product id is %s' % blog_post.content)

class SignUp(Handler):


	def validate_field(self,text, regex_pattern):
		regex_pattern = re.compile(r"%s" % regex_pattern)
		return regex_pattern.match(text)

	def display_validation_error(self,identifier, valid):
		if(not valid):
			return "The %s is invalid!" % identifier
		else:
			return ""

	def render_signup(self,username="",password="",verify_password="",email="",user_msg="",pswd_msg="",ver_pswd_msg="",email_msg=""):
		self.render("login.html",username=username,password=password,verify_password=verify_password,email=email,user_msg=user_msg,pswd_msg=pswd_msg,ver_pswd_msg=ver_pswd_msg,email_msg=email_msg)

	def get (self):
		self.render_signup()

	def post(self):
		username = self.request.get('username')
		password = self.request.get('password')
		verify_password = self.request.get('verify')
		email = self.request.get('email')

		valid_username = self.validate_field(username,"^[a-zA-Z0-9_-]{3,20}$")
		valid_password = self.validate_field(password, "^.{3,20}$")
		valid_email = self.validate_field(email,"^[\S]+@[\S]+\.[\S]+$")
		password_match = (password == verify_password)

		if (valid_username and valid_password  and password_match):
			#self.response.out.write("Hello")
			user = User.by_name(username)
			if user:
				msg = 'That user already exists!'
				self.render_signup(username=username,user_msg=msg)
			else:
				u = User.register(username,password,email)
				u.put()
				self.login(u)
				self.redirect('/welcome')
		else:
			user_msg = self.display_validation_error("username",valid_username)
			password_msg = self.display_validation_error("password",valid_password)
			match_msg = ""
			if not password_match:
				match_msg = "The passwords don't match!"
			email_msg = self.display_validation_error("email",valid_email)
			self.render_signup(username=username,password=password,verify_password=verify_password,
				email=email,user_msg=user_msg,pswd_msg=password_msg,ver_pswd_msg=match_msg,email_msg=email_msg)


class WelcomeHandler(Handler):
	def get(self):
		uid = self.read_cookie('user_id')
		user = User.get_by_id(int(uid))
		if user:
			self.write("Welcome, %s" % user.name)
		else:
			self.redirect('/signup')

class LoginHandler(Handler):

	def get(self):
		self.render('login_form.html')

	def post(self):
		username = self.request.get('username')
		password = self.request.get('password')

		user = User.login(username,password)
		if user:
			self.login(user)
			self.redirect('/welcome')
		else:
			msg = 'Invalid Login'
			self.render('login_form.html',error_msg=msg)


class LogoutHandler(Handler):

	def get(self):
		self.logout()
		self.redirect('/signup')

app = webapp2.WSGIApplication([('/',MainPage),
	('/newpost',NewBlog),
	(r'/(\d+)',BlogHandler),
	 ('/signup',SignUp), 
	 ('/welcome',WelcomeHandler),
	 ('/login',LoginHandler),
	 ('logout',LogoutHandler),
	 ],debug=True)