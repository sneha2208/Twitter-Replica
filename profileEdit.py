import webapp2
import jinja2
from verification import Verification
import os
from thirdModel import UserModel
from google.appengine.ext import ndb
from datetime import datetime

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class ProfileEdit(webapp2.RequestHandler):
    def get(self):
        template_values = Verification(self.request.uri).userTemplateVals()
        if template_values['user'] == '' or template_values['user'] is None:
            template = JINJA_ENVIRONMENT.get_template('main.html')
            self.response.write(template.render(template_values))
        else:
            if template_values['username'] == '' or template_values['username'] is None:
                self.redirect('/register')
            else:
                user_model = UserModel()
                user_key = ndb.Key(UserModel, template_values['username'])
                user_model.key = user_key
                get_user = user_key.get()
                template_values['userInfo'] = get_user
                template = JINJA_ENVIRONMENT.get_template('profile-edit.html')
                self.response.write(template.render(template_values))

    def post(self):
        template_values = Verification(self.request.uri).userTemplateVals()

        if template_values['user'] == '' or template_values['user'] is None:
            template = JINJA_ENVIRONMENT.get_template('main.html')
            self.response.write(template.render(template_values))
        else:
            action = self.request.get('button')
            if action.lower() == 'submit':
                first_name = self.request.get('first_name')
                last_name = self.request.get('last_name')
                user_profile = self.request.get('user_profile')

                thirdModel = UserModel()
                user_key = ndb.Key(UserModel, template_values['username'])
                thirdModel.key = user_key
                get_user = user_key.get()
                get_user.first_name = first_name
                get_user.last_name = last_name
                if len(user_profile) > 280:
                    user_model = UserModel()
                    user_key = ndb.Key(UserModel, template_values['username'])
                    user_model.key = user_key
                    get_user = user_key.get()
                    template_values['userInfo'] = get_user
                    template_values['err_msg'] = 'Profile content can not be more than 280 characters'
                    template = JINJA_ENVIRONMENT.get_template('profile-edit.html')
                    self.response.write(template.render(template_values))
                else:
                    get_user.user_profile = user_profile
                    get_user.put()
                    self.redirect('/profile')
