import sys
sys.path.insert(0, "/home/wsgi/public_wsgi/biobackend")
from bio_backend.app import create_app
application = create_app()