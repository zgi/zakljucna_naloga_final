#!/usr/bin/env python
from google.appengine.api import users
from google.appengine.api import urlfetch
from models import Mail
import os
import jinja2
import webapp2
import json


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        ip = self.request.remote_addr

        user_loc= urlfetch.fetch('https://ipapi.co/' + ip + '/latlong/')
        user_loc_split = user_loc.content.split(',')
        lat = user_loc_split[0]
        lon = user_loc_split[1]

        vreme_url = 'http://api.openweathermap.org/data/2.5/weather?lat=' + lat + '&lon=' + lon + '&units=metric&appid=66892177070053d1b9db47015ed90142'
        result = urlfetch.fetch(vreme_url)
        vreme = json.loads(result.content)

        if user:
            logiran = True
            logout_url = users.create_logout_url('/')
            params = {"logiran": logiran, "logout_url": logout_url, "user": user}
            params['vreme'] = vreme
        else:
            logiran = False
            login_url = users.create_login_url('/')
            params = {"logiran": logiran, "login_url": login_url, "user": user}

        return self.render_template('pozdrav.html', params)


class NovoSporociloHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            logiran = True
            logout_url = users.create_logout_url('/')
            params = {"logiran": logiran, "logout_url": logout_url, "user": user}
        else:
            logiran = False
            login_url = users.create_login_url('/')
            params = {"logiran": logiran, "login_url": login_url, "user": user}
        if self.request.get('email'):
            novo_sporocilo_za = self.request.get('email')
            params['email'] = novo_sporocilo_za
        return self.render_template("novo_sporocilo.html", params)

    def post(self):
        user = users.get_current_user()
        if user:
            try:
                posiljatelj = user.email().lower()
                naslovnik = self.request.get('naslovnik').replace('<script>', '').replace('</script>', '').lower()
                zadeva = self.request.get('zadeva').replace('<script>', '').replace('</script>', '')
                sporocilo = self.request.get('sporocilo').replace('<script>', '').replace('</script>', '')
                kratko_sporocilo = (sporocilo[:75] + '...') if len(sporocilo) > 75 else sporocilo
                podatki = Mail(posiljatelj=posiljatelj, naslovnik=naslovnik, zadeva=zadeva, sporocilo=sporocilo, kratko_sporocilo=kratko_sporocilo, poslano=True)
                podatki.put()
                return self.redirect_to('poslano')
            except:
                return self.write('Predolgo sporocilo...jeba! Skrajsaj, poskusi bit bol jedernat =)')


class PrejetoHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            logiran = True
            logout_url = users.create_logout_url('/')
            params = {"logiran": logiran, "logout_url": logout_url, "user": user}
        else:
            logiran = False
            login_url = users.create_login_url('/')
            params = {"logiran": logiran, "login_url": login_url, "user": user}

        sporocila = Mail.query(Mail.izbrisano == False, Mail.naslovnik == user.email()).fetch()


        podatki = {'sporocila': sporocila}
        podatki.update(params)
        return self.render_template("prejeto.html", params=podatki)


class PreberiSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        user = users.get_current_user()
        if user:
            logiran = True
            logout_url = users.create_logout_url('/')
            params = {"logiran": logiran, "logout_url": logout_url, "user": user}
        else:
            logiran = False
            login_url = users.create_login_url('/')
            params = {"logiran": logiran, "login_url": login_url, "user": user}

        sporocilo = Mail.get_by_id(int(sporocilo_id))
        sporocilo.prebrano = True
        sporocilo.put()

        podatki = {'sporocilo': sporocilo}
        podatki.update(params)
        return self.render_template("preberi.html",params=podatki)


class PoslanoHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            logiran = True
            logout_url = users.create_logout_url('/')
            params = {"logiran": logiran, "logout_url": logout_url, "user": user}
        else:
            logiran = False
            login_url = users.create_login_url('/')
            params = {"logiran": logiran, "login_url": login_url, "user": user}
        sporocila = Mail.query(Mail.poslano == True, Mail.posiljatelj == user.email(), Mail.izbrisano == False).fetch()
        podatki = {'sporocila': sporocila}
        podatki.update(params)
        return self.render_template("poslano.html",params=podatki)


class IzbrisanoHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            logiran = True
            logout_url = users.create_logout_url('/')
            params = {"logiran": logiran, "logout_url": logout_url, "user": user}
        else:
            logiran = False
            login_url = users.create_login_url('/')
            params = {"logiran": logiran, "login_url": login_url, "user": user}
        sporocila = Mail.query(Mail.izbrisano == True).fetch()
        podatki = {'sporocila': sporocila}
        podatki.update(params)
        return self.render_template("izbrisano.html",params=podatki)
    def post(self, sporocilo_id):
        sporocilo = Mail.get_by_id(int(sporocilo_id))
        sporocilo.izbrisano = True
        sporocilo.put()
        return self.redirect_to('prejeto')

class Delete4EvvahHandler(BaseHandler):
    def post(self, sporocilo_id):
        sporocilo = Mail.get_by_id(int(sporocilo_id))
        sporocilo.key.delete()
        return self.redirect_to('izbrisano')

class StikiHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            logiran = True
            logout_url = users.create_logout_url('/')
            params = {"logiran": logiran, "logout_url": logout_url, "user": user}

        else:
            logiran = False
            login_url = users.create_login_url('/')
            params = {"logiran": logiran, "login_url": login_url, "user": user}

        stiki = []
        sporocila = Mail.query()

        poslana_sporocila = sporocila.filter(Mail.posiljatelj == user.email())
        poslana_sporocila.fetch()


        for stik in poslana_sporocila:
            if stik.naslovnik not in stiki:
                stiki.append(stik.naslovnik)

        prejeta_sporocila = sporocila.filter(Mail.naslovnik == user.email())
        prejeta_sporocila.fetch()

        for stik in prejeta_sporocila:
            if stik.posiljatelj not in stiki:
                stiki.append(stik.posiljatelj)

        podatki = {'naslovi': stiki}
        podatki.update(params)
        return self.render_template("stiki.html",params=podatki)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/novo', NovoSporociloHandler),
    webapp2.Route('/prejeto', PrejetoHandler, name='prejeto'),
    webapp2.Route('/preberi/<sporocilo_id:\d+>', PreberiSporociloHandler),
    webapp2.Route('/poslano', PoslanoHandler, name='poslano'),
    webapp2.Route('/izbrisano', IzbrisanoHandler, name='izbrisano'),
    webapp2.Route('/izbrisi/<sporocilo_id:\d+>', IzbrisanoHandler),
    webapp2.Route('/delete4evvah/<sporocilo_id:\d+>', Delete4EvvahHandler),
    webapp2.Route('/stiki', StikiHandler),
], debug=True)
