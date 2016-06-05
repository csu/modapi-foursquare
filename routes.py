import time

from flask import Blueprint, request, jsonify
import foursquare

from backup import backup_all_checkins
from common import require_secret
from config import config
import secrets

module = Blueprint(config['module_name'], __name__)

client = foursquare.Foursquare(access_token=secrets.FOURSQUARE_ACCESS_TOKEN)

def perform_checkins(places):
    for place in places:
        client.checkins.add(params={'venueId': place})
        time.sleep(0.5)

@module.route('/')
@require_secret
def get_all_checkins():
    return jsonify(client.users.checkins())

@module.route('/checkin')
@module.route('/checkin/')
@require_secret
def do_checkins():
    places = request.args.get('p').split(',')
    perform_checkins(places)
    return jsonify({'status': 'ok', 'places': places})

@module.route('/recent')
@module.route('/recent/')
@require_secret
def get_recent():
    latest = client.users.checkins(params={'limit': 3})['checkins']['items']
    latest = [i['venue']['name'] for i in latest]

    title = ". ".join(latest)
    message = "<b>Latest Checkins</b><br>"
    message += "<br>".join(latest)

    notifier.send(message, title=title, source="ModApi")

    return jsonify({'status': 'ok'})

@module.route('/backup')
@module.route('/backup/')
@require_secret
def backup_all_checkins():
    checkins = backup_all_checkins(client, uploader)

    return jsonify({'status': 'ok', 'checkins': len(checkins)})