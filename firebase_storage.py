import requests
from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from pyrebase import initialize_app
from django.conf import settings

class FirebaseStorage(Storage):
    def __init__(self):
        self.firebase = initialize_app(settings.FIREBASE_CONFIG)
        self.storage = self.firebase.storage()

    def _open(self, name, mode='rb'):
        url = self.storage.child(name).get_url(None)
        response = requests.get(url)
        return ContentFile(response.content)

    def _save(self, name, content):
        self.storage.child(name).put(content)
        return name

    def url(self, name):
        return self.storage.child(name).get_url(None)