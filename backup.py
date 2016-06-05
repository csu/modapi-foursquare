import secrets

def backup_all_checkins(client, uploader):
    checkins = [c for c in client.users.all_checkins()]
    uploader.quick_upload(checkins, file_prefix='foursquare',
        folder=secrets.BACKUP_FOLDER_ID)

    return checkins

if __name__ == '__main__':
  import foursquare
  from uploader import gdrive
  client = foursquare.Foursquare(access_token=secrets.FOURSQUARE_ACCESS_TOKEN)
  uploader = gdrive.GDriveUploader()
  backup_all_checkins(client, uploader)