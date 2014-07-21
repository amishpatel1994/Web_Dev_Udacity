import os
import jinja2
import webapp2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape=True)


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

app = webapp2.WSGIApplication([('/',MainPage),('/newpost',NewBlog),(r'/(\d+)',BlogHandler),],debug=True)