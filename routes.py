import datetime
import json
import tempfile
import thread
import time

from flask import Blueprint, request, jsonify
import foursquare

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
def backup_all_checkins():
    checkins = [c for c in client.users.all_checkins()]

    temp_file = tempfile.NamedTemporaryFile()
    temp_file.write(json.dumps(checkins))

    filename = 'foursquare-%s.json' % datetime.date.today()
    folder = secrets.BACKUP_FOLDER_ID
    uploader.upload(temp_file.name, title=filename, parent=folder)

    temp_file.close()

    return jsonify({'status': 'ok', 'checkins': len(checkins)})