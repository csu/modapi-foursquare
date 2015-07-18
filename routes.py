import thread
import time

from flask import Blueprint, request, abort, jsonify
import foursquare

from config import config
import secrets

module = Blueprint(config['module_name'], __name__)

client = foursquare.Foursquare(access_token=secrets.FOURSQUARE_ACCESS_TOKEN)

def perform_checkins(places):
    for place in places:
        client.checkins.add(params={'venueId': place})
        time.sleep(0.5)


@module.route('/')
def get_checkins():
    if secret_key and secret_key_value:
        val = request.args.get(secret_key)
        if val != secret_key_value:
            abort(403)
    return jsonify(client.users.checkins())

@module.route('/checkin')
@module.route('/checkin/')
def checkin():
    if secret_key and secret_key_value:
        val = request.args.get(secret_key)
        if val != secret_key_value:
            abort(403)

    places = request.args.get('p').split(',')
    perform_checkins(places)
    return jsonify({'status': 'ok', 'places': places})