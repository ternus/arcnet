import os
import sys
sys.path.append('/srv/')
sys.path.append('/srv/arcnet/')

sys.stdout = sys.stderr
os.environ['DJANGO_SETTINGS_MODULE'] = 'arcnet.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
