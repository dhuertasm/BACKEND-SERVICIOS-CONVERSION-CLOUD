import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(os.getenv('MEDIAFILE', APP_ROOT), 'mediafiles') # "/consumer"
