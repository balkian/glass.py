from django.db import models
import uuid
# Create your models here.

from push_notifications.models import Device
from user import User as GlassUser
from .utils import app
from .exceptions import *


def code_generate():
    u = uuid.uuid4().bytes.encode("base64")
    return u


class GlassDeviceManager(models.Manager):
    def get_query_set(self):
        return GlassDeviceQuerySet(self.model)


class GlassDeviceQuerySet(models.query.QuerySet):
    def send_message(self, message, **kwargs):
        if self:
            for i in self:
                i.send(message, **kwargs)


class Glass(Device):
    access_token = models.CharField(verbose_name="Access Token",
                                    max_length=255, blank=True, null=True)
    refresh_token = models.CharField(verbose_name="Refresh Token",
                                     max_length=255, blank=True, null=True)
    objects = GlassDeviceManager()

    def send_message(self, message=None, **kwargs):
        if message is not None:
            kwargs["text"] = message["data"]
        if "menuItems" not in kwargs:
            kwargs["menuItems"] = [{"action": "DELETE"} ]
        tokens = {"access_token": self.access_token,
                  "refresh_token": self.refresh_token}
        user = GlassUser(app=app, tokens=tokens)
        try:
            user.timeline.post(**kwargs)
        except RefreshTokenException, e:
            # Access token is no longer valid : refresh token
            tokens = user.refresh_tokens()
            self.access_token = tokens["access_token"]
            self.refresh_token = tokens["refresh_token"]
            self.save()
            user.timeline.post(**kwargs)

    def __repr__(self):
        return repr(self.to_dict())
