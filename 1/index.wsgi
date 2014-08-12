import sae
from mysite import wsgi
import os
import pylibmc
import sys
sys.modules['memcache'] = pylibmc
root = os.path.dirname(__file__)

sys.path.insert(0, os.path.join(root, 'site-packages'))
application = sae.create_wsgi_app(wsgi.application)
