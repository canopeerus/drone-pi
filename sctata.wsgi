import os, sys, logging
logging.basicConfig(stream=sys.stderr)

PROJECT_DIR = '/var/www/sctata'

activate_this = os.path.join(PROJECT_DIR, 'bin', 'activate_this.py')
#execfile(activate_this, dict(__file__=activate_this))
sys.path.append(PROJECT_DIR)

from main import app as application
