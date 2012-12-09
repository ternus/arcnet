import os
import sys
sys.path.append('/srv/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'arcnet.settings'



from django.core import management 
from django.db import connection 
cursor = connection.cursor() 
    # don't delete these tables 
    # note that I'm also keeping auth_user 
current_tables = connection.introspection.table_names() 
for table in current_tables: 
    try: 
        cursor.execute("drop table %s" % table) 
    except: 
  	  	  pass
management.call_command('syncdb') 
