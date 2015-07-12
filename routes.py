from flask import Blueprint, request, abort
from config import config

module = Blueprint(config['module_name'], __name__)

@module.route('/')
def index():
    if secret_key and secret_key_value:
        val = request.args.get(secret_key)
        print val
        if val != secret_key_value:
            abort(403)
    return 'hello world'