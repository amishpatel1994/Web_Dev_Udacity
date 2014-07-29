import os
import webapp2
import jinja2
import urllib2
from xml.dom import minidom


from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape=True)



class Handler(webapp2.RequestHandler):
	def write(self,*a,**kw):
		self.response.out.write(*a,**kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self,template,**kw):
		self.write(self.render_str(template, **kw))


def get_coords(xml):
    content = minidom.parseString(xml)
    location = content.getElementsByTagName("gml:coordinates")
    if location and location[0].childNodes[0].nodeValue:
    	coords = (location[0].childNodes[0].nodeValue).split(',')
    	return (coords[1],coords[0])
    return

GMAPS_URL = "http://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false&"

def gmaps_img(points):
	markers = '&'.join('markers=%s,%s' % (p.lat,p.lon) for p in points)
	return GMAPS_URL + markers

IP_URL = "http://api.hostip.info/?ip="
def get_coordinate(ip):
	ip = "4.2.2.2"
	url = IP_URL + ip
	content = None
	try:
		content = urllib2.urlopen(url).read()
	except URLError:
		return

	if content:
		#parse the xml and fin the coordinates
		(lat,lng) = get_coords(content)
		return db.GeoPt(lat,lng)

class Art(db.Model):
	title = db.StringProperty(required = True)
	art = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	coordinates = db.GeoPtProperty()

class MainPage(Handler):
	def render_front(self,title="",error="",art=""):
		arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC LIMIT 10")
		
		arts = list(arts)
		points = []
		for a in arts:
			if a.coordinates:
				points.append(a.coordinates)
		img_url = None
		if points:
			img_url = gmaps_img(points)


		#find which arts have coors
		#if we have any arts coords, make an image url

		self.render("main.html",title=title,error=error,art=art,arts=arts, img_url=img_url)

	def get(self):
		#self.write(self.request.remote_addr)
		#self.write(repr(get_coordinate(self.request.remote_addr)))
		self.render_front()

	def post(self):
		title = self.request.get('title')
		art = self.request.get('art')

		if art and title:
			a = Art(title=title,art=art)
			#get user's coordinate from their ip
			coordinates = get_coordinate(self.request.remote_addr)
			#if we get the coordinates, we add it to the map
			if coordinates:
				a.coordinates = coordinates
			a.put()

			self.redirect("/")
		else:
			error = "we need both a title and some art work!"
			self.render_front(error=error,title=title,art=art)


app = webapp2.WSGIApplication([('/',MainPage),],debug=True)