from google.appengine.ext import ndb

class Mail(ndb.Model):
    sporocilo = ndb.StringProperty()
    kratko_sporocilo = ndb.StringProperty()
    zadeva = ndb.StringProperty()
    posiljatelj = ndb.StringProperty()
    naslovnik = ndb.StringProperty()
    izbrisano = ndb.BooleanProperty(default=False)
    prebrano = ndb.BooleanProperty(default=False)
    poslano = ndb.BooleanProperty(default=False)
    nastanek = ndb.DateTimeProperty(auto_now_add=True)
