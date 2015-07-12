import foursquare

import secrets

client = foursquare.Foursquare(access_token=secrets.FOURSQUARE_ACCESS_TOKEN)

print client.venues('')