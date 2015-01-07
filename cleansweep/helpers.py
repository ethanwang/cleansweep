"""Helpers functions to use in templates.

Includes template filters and context processors.
"""
from flask import (request, session, g, url_for)
import datetime
import humanize
from .app import app
from .widgets import render_widget
from .models import Member, Place, PlaceType
from . import oauth
from .voterlib import VoterDB
from . import stats
import json

sidebar_entries = []

@app.template_filter('pluralize')
def pluralize(name):
    """Returns plural form of name.

        >>> pluralize('Polling Booth')
        'Polling Booths'
        >>> pluralize('Assembly Constituency')
        'Assembly Constituencies'
    """
    if name.endswith("y"):
        return name[:-1] + "ies"
    else:
        return name + 's'

@app.template_filter()
def naturaltime(datetime):
    return humanize.naturaltime(datetime)


@app.template_filter()
def json_encode(value):
    return json.dumps(value)


def get_current_user():
    if session.get('user'):
        return Member.find(email=session['user'])

@app.context_processor
def helpers():
    return {
        "len": len,
        "request_path": request.path,
        "widget": render_widget,
        "user": get_current_user(),
        "get_toplevel_places": Place.get_toplevel_places,
        "get_config": app.config.get,
        "get_oauth_providers": oauth.get_oauth_providers,
        "permissions": getattr(g, "permissions", []),
        "voterdb": VoterDB(app.config["VOTERDB_URL"]),
        "sidebar_entries": sidebar_entries,
        "get_stats": stats.get_stats,
        "get_stat": stats.get_stat,
        "today": datetime.datetime.today(),
        "yesterday": datetime.datetime.today() - datetime.timedelta(days=1),
    }

@app.context_processor
def place_types():
    types = PlaceType.all()
    return dict((t.short_name, t) for t in types)