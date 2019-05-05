import webapp2
import jinja2
import os
from verification import Verification
from home import Home, PhotoUploadHandler
from register import Register
from profile import Profile
from profileEdit import ProfileEdit
from tweetEdit import TweetEdit
from searchUser import SearchUser
from searchContent import SearchContent

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class MainPage(webapp2.RequestHandler):
    def get(self):
        template_values = Verification(self.request.uri).userTemplateVals()
        if template_values['user'] == '' or template_values['user'] is None:
            template = JINJA_ENVIRONMENT.get_template('main.html')
            self.response.write(template.render(template_values))
        else:
            if template_values['username'] == '' or template_values['username'] is None:
                self.redirect('/register')
            else:
                self.redirect('/home')


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/home', Home),
    ('/register', Register),
    ('/profile', Profile),
    ('/profile-edit', ProfileEdit),
    ('/tweet-edit', TweetEdit),
    ('/search-user', SearchUser),
    ('/search-content', SearchContent),
    ('/upload', PhotoUploadHandler),
], debug=True)
