from django.conf.urls.defaults import *

#Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth.models import User
admin.autodiscover()
admin.site.unregister(User)


urlpatterns = patterns('',
    # Example:
    # (r'^arcnet/', include('arcnet.foo.urls')),

    (r'^$', 'arcnet.media.views.homefeed'),
    (r'^log/$', 'arcnet.media.views.myfeed'),

    (r'^arkipedia/$', 'arcnet.pedia.views.entries'),
    (r'^arkipedia/(.+)$', 'arcnet.pedia.views.entry'),
    
    (r'^research/$', 'arcnet.research.views.research_overview'),
    (r'^research/published/$', 'arcnet.research.views.published'),
    #(r'^research/tree/$', 'arcnet.research.views.tech_tree'),
    (r'^research/tree/(.)$', 'arcnet.research.views.tech_tree'),
    (r'^research/unlock/', 'arcnet.research.views.unlock'),
    (r'^research/theorize/', 'arcnet.research.views.theorize'),
    (r'^research/publish/(\w{5})$', 'arcnet.research.views.publish'),
    (r'^research/(\w{5})$', 'arcnet.research.views.tech'),
    (r'^research/(\w{5})/(\d)$', 'arcnet.research.views.research'),

    (r'^char/$', 'arcnet.core.views.profile'),
    (r'^char/browse$', 'arcnet.core.views.profile_browser'),
    (r'^char/browse/$', 'arcnet.core.views.profile_browser'),
    (r'^char/(.+)$', 'arcnet.core.views.profile'),

    (r'^mail/$', 'arcnet.mail.views.allmail'),
    (r'^mail/read/(.+)$', 'arcnet.mail.views.readmail'),
    (r'^mail/send/$', 'arcnet.mail.views.sendmail'),
    (r'^mail/sent/$', 'arcnet.mail.views.sentmail'),


    (r'^fame/$', 'arcnet.media.views.famouspeople'),

    (r'^rumors/', 'arcnet.cyber.views.rumors'),


    (r'^opinion/$', 'arcnet.media.views.allsupport'),
    (r'^opinion/agents/$', 'arcnet.media.views.agents'),
    (r'^opinion/candidate/$', 'arcnet.media.views.candidate'),
    (r'^opinion/endorse/$', 'arcnet.media.views.endorse'),
    (r'^opinion/(.+)$', 'arcnet.media.views.subject'),

    (r'^media/$', 'arcnet.media.views.mediafeed'),
    (r'^media/all/$', 'arcnet.media.views.allmedia'),
    (r'^media/old/(.+)/(.+)$', 'arcnet.media.views.mediafeed'),
    (r'^media/(\d+)$', 'arcnet.media.views.readpost'),
    (r'^media/post/text$', 'arcnet.media.views.textpost'),
    (r'^media/post/image$', 'arcnet.media.views.imagepost'),

    (r'^gm/audiopost$', 'arcnet.media.views.audiopost'),


    (r'^login/', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    (r'^logout/', 'django.contrib.auth.views.logout', {'next_page': '/login/'}),
    
#    (r'^files/', 'arcnet.cyber.views.files'),
#    (r'^files/view/(.+)$', 'arcnet.cyber.views.view_file'),
#    (r'^files/delete/(.+)$', 'arcnet.cyber.views.view_file'),

    (r'^net/$', 'arcnet.cyber.views.net_home'),            
    (r'^net/computrons/$', 'arcnet.cyber.views.computrons'),            
   # (r'^net/programs$', 'arcnet.cyber.views.my_programs'),
   # (r'^net/unpack$', 'arcnet.cyber.views.unpack'),
   # (r'^net/integrate/(.+?)/(.+)$', 'arcnet.cyber.views.integrate'),


    (r'^net/(.+)/server$', 'arcnet.cyber.views.access_computer'),
    (r'^net/(.+)/analyze$', 'arcnet.cyber.views.full_ice'),
    (r'^net/(.+)/ice/(.+)/(.)$', 'arcnet.cyber.views.render_ice'),
    (r'^net/(.+)/$', 'arcnet.cyber.views.hack_computer'),
    
#    (r'^arcnet/home/', 'arcnet.core.views.home'),



    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

#    (r'^tinymce/', include('tinymce.urls')),


#    (r'^/$', ) #home
)
