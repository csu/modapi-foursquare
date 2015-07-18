import thread
import time

from flask import Blueprint, request, abort, jsonify
import foursquare

from config import config
import secrets

module = Blueprint(config['module_name'], __name__)

client = foursquare.Foursquare(access_token=secrets.FOURSQUARE_ACCESS_TOKEN)

def secret_correct():
    if secret_key and secret_key_value:
        val = request.args.get(secret_key)
        if val == secret_key_value:
            return True
    return False

def perform_checkins(places):
    for place in places:
        client.checkins.add(params={'venueId': place})
        time.sleep(0.5)

@module.route('/')
def get_all_checkins():
    if not secret_correct():
        abort(403)
    return jsonify(client.users.checkins())

@module.route('/checkin')
@module.route('/checkin/')
def do_checkins():
    if not secret_correct():
        abort(403)

    places = request.args.get('p').split(',')
    perform_checkins(places)
    return jsonify({'status': 'ok', 'places': places})

@module.route('/recent')
@module.route('/recent/')
def get_recent():
    if not secret_correct():
        abort(403)

    latest = client.users.checkins(params={'limit': 3})['checkins']['items']
    latest = [i['venue']['name'] for i in latest]

    title = ". ".join(latest)
    message = "<b>Latest Checkins<b><br>"
    message += "<br>".join(latest)

    notifier.send(message, title=title, source="ModApi")

    return jsonify({'status': 'ok'})