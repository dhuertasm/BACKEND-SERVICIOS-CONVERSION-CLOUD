import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(os.getenv('MEDIAFILE', APP_ROOT), 'mediafiles') # "/consumer"
UPLOAD_FOLDER_BUCKET = 'nube-media-files/mediafiles/'
BUCKET_KEY_GCP = os.path.join(os.getenv('variable',APP_ROOT),'core')