
# Create your views here.

from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import render_to_response, get_object_or_404
from arcnet.core.models import *
from media.models import *

class Trance():
    pass

@login_required
def profile(request, cname=None):
    if cname is None:
        char = request.user
    else:
        char = get_object_or_404(Character, username=cname)

    agent = Agent.objects.get(direct=True,controller=char)
    positions = Position.objects.filter(agent=agent).order_by("-time")
    myposts = Post.objects.filter(author=char).order_by("-time")
    theposts = char.characters_posts.all().order_by("-time")
    endorsers = Agent.objects.filter(candidate=char)

    return render_to_response("char.html", {'endorsers':endorsers, 'endorsement':agent.candidate, 'char':char, 'positions':positions, 'myposts':myposts, 'theposts':theposts}, context_instance=RequestContext(request))


def profile_browser(request):
    chars = Character.objects.filter(visible=True)
    return render_to_response("profile-browser.html", {'characters':chars,}, context_instance=RequestContext(request))



@login_required
def home(request):
    return render_to_response("home.html", {}, context_instance=RequestContext(request))
    
