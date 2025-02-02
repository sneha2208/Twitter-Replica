import webapp2
import jinja2
from google.appengine.ext import ndb
import os
from datetime import datetime
from verification import Verification
from thirdModel import UserModel


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class Register(webapp2.RequestHandler):
    def get(self):
        template_values = Verification(self.request.uri).userTemplateVals()
        if template_values['user'] == '' or template_values['user'] is None:
            template = JINJA_ENVIRONMENT.get_template('main.html')
            self.response.write(template.render(template_values))
        else:
            if template_values['username'] == '' or template_values['username'] is None:
                template = JINJA_ENVIRONMENT.get_template('register.html')
                self.response.write(template.render(template_values))
            else:
                self.redirect('/')

    def post(self):
        template_values = Verification(self.request.uri).userTemplateVals()

        if template_values['user'] == '' or template_values['user'] is None:
            template = JINJA_ENVIRONMENT.get_template('main.html')
            self.response.write(template.render(template_values))
        else:
            action = self.request.get('button')
            if action.lower() == 'submit':
                err_msg = ''
                user_name = self.request.get('userName')
                first_name = self.request.get('first_name')
                last_name = self.request.get('last_name')
                user_profile = self.request.get('user_profile')
                if user_name == '' or user_name is None:
                    err_msg = 'Username is required.'
                else:
                    if template_values['username'] == '' or template_values['username'] is None:
                        thirdModel = UserModel()
                        user_email = "%s" %(template_values['user'])
                        user_key = ndb.Key(UserModel, user_name)
                        thirdModel.key = user_key
                        get_user = user_key.get()
                        if get_user is None:
                            thirdModel.email = user_email
                            thirdModel.user_name = user_name
                            thirdModel.first_name = first_name
                            thirdModel.last_name = last_name
                            if len(user_profile) > 280:
                                err_msg = 'Profile content can not be more than 280 characters'
                            else:
                                thirdModel.user_profile = user_profile
                                thirdModel.put()
                                self.redirect('/')
                        else:
                            err_msg = 'This username is already taken.'
                    else:
                        err_msg = 'You can not change the user name.'
                template_values['err_msg'] = err_msg
                template = JINJA_ENVIRONMENT.get_template('register.html')
                self.response.write(template.render(template_values))
