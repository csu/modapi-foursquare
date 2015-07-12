import foursquare

import secrets

client_id = secrets.FOURSQUARE_CLIENT_ID
client_secret = secrets.FOURSQUARE_CLIENT_SECRET
redirect_uri = secrets.FOURSQUARE_REDIRECT_URI

client = foursquare.Foursquare(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

# Use this first:
# auth_uri = client.oauth.auth_url()
# print auth_uri

# Then this, with the code from the first step:
access_token = client.oauth.get_token('')
print access_token