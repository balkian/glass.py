from .app import Application
import configs
from django.shortcuts import redirect
from django.template import Template
import logging
log = logging.getLogger(__name__)


class DjangoWrapper(object):
    Template = Template
    logger = log

    def redirect(self, *args, **kwargs):
        return redirect(*args, **kwargs)

    def get_request(*args, **kwargs):
        return args[1].GET


wrapper = DjangoWrapper()

app = Application(
    name="Django",
    client_id=configs.CLIENT_ID,
    client_secret=configs.CLIENT_SECRET,
    web=wrapper
)


app.host = "dev.pastetophone.com"
app.secure = False
