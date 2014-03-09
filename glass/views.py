from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import logging
log = logging.getLogger(__name__)

from .models import Glass
from .utils import app

#@login_required
def oauth_authorize(*args, **kwargs):
    log.debug("Authorising")
    return app._oauth_authorize(*args, **kwargs)

@app.subscriptions.login
def login(user):
    log.info("Glass User: %s" % user.token)
    glass = Glass(name="Google Glass", ack=True, user=user.profile()["email"], access_token=user.tokens["access_token"], refresh_token=user.tokens["refresh_token"])
    glass.save()
    card = {
        "html": "<article>\n    <img src=\"http://pastetophone.com/static/landing-page/img/mac_to_phone.png\"></img><section> <img src=\"http://pastetophone.com/static/img/logo-web.png\" width=\"5%\"> Welcome to \n PasteToPhone </section>\n</article>\n",
        "notification": {
            "level": "DEFAULT"
        },
        "menuItems": [ {
            "action": "DELETE"
        } ]
    }
    glass.send_message(**card)

#@login_required
def oauth_callback(*args, **kwargs):
    log.debug("Callback oauth")
    resp = app._oauth_callback(*args, **kwargs)
    return HttpResponse(resp)
