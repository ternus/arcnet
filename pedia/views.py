# Create your views here.

from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render_to_response, get_object_or_404

from arcnet.pedia.models import Entry

class Trance():
    pass

def entry(request, name):
    e = get_object_or_404(Entry, name=name)
    return render_to_response("pedia.html", {'e':e}, context_instance=RequestContext(request))

def entries(request):
    entries = Entry.objects.all().order_by("name")
#    t = Trance()
#    t.heading = "test"
#    t.caption = "test2"
    return render_to_response("pedialist.html", {'entries':entries}, context_instance=RequestContext(request))
