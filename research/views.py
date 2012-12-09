# Create your views here.

from django import forms
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import render_to_response, get_object_or_404
from arcnet.core.models import *
from arcnet.research.models import *
from elog.models import *
from django.shortcuts import render_to_response, get_object_or_404
import pydot
import settings
from cyber.defaults import *
from defaults import *
from datetime import datetime


@login_required
def tech(request, techid):

    t = get_object_or_404(Tech, startCode=techid)
    if t.is_published() and not Research.objects.filter(character=request.user, tech=t).exists():
        r = Research(character=request.user, tech=t, state=STATE_HYPOTHESIS)
        r.save()
    r = get_object_or_404(Research, character=request.user, tech__startCode=techid)

    children=None

    if r.state >= STATE_CONCLUSION:
        children = []
        for nt in Tech.objects.all():
            if r.tech in nt.prereqs.all():
                children += [nt]
    return render_to_response("tech.html", {'r': r, 'children':children}, context_instance=RequestContext(request))
    

techcolors = {
    1: ["white", "black"],
    2: ["#ddffdd", "black"],
    3: ["#ddddff", "black"],
    4: ["#ffffd0", "black"],
    5: ["#ffddaa", "black"],
    6: ["#ffdddd", "black"],
    7: ["#999999", "black"]
}

@login_required
def tech_tree(request, tree=None):
    if tree:
        techs = Tech.objects.filter(tree=tree).exclude(publishedBy=None)
    else:
        return HttpResponseRedirect("/") #fuck you
        techs = Tech.objects.all().exclude(publishedBy=None)
    edges = []
    g = pydot.Dot(bgcolor="#e6e4da", rankdir="LR", splines="true", levels="7")
    techlist = []
    for tech in techs:
        techlist += [tech]
        g.add_node(pydot.Node(tech.box(), 
                              fontsize="9", 
                              shape="rect", 
                              style="filled", 
                              fillcolor=techcolors[tech.difficultyLevel()][0],
                              fontcolor=techcolors[tech.difficultyLevel()][1],
                              color=techcolors[tech.difficultyLevel()][1], 
                              level=str(tech.difficultyLevel())))
    for tech in techs:
        for pre in tech.prereqs.all():#.exclude(publishedBy=None):
            if not pre in techlist:
                g.add_node(pydot.Node(pre.box(), 
                           fontsize="9", 
                           shape="diamond", 
                           style="filled, dotted", 
                           fillcolor=techcolors[pre.difficultyLevel()][0],
                           fontcolor=techcolors[pre.difficultyLevel()][1],
                           color=techcolors[pre.difficultyLevel()][1], 
                           level=str(pre.difficultyLevel())))
            g.add_edge(pydot.Edge(pre.box(), 
                                  tech.box(), 
                                  arrowhead="vee", 
                                  arrowsize=".5"))
    g.write_png(str(settings.AUTOGEN_MEDIA_ROOT)+'techtree.png', prog='dot')
    return render_to_response("techtree.html", {}, context_instance=RequestContext(request))

class StartForm(forms.Form):
    pass

@login_required
def publish(request, tech):
    tech = get_object_or_404(Tech, startCode=tech)
    if tech.is_published():
        messages.error(request, "That tech is already published!")
        return HttpResponseRedirect("/research/")

    r = get_object_or_404(Research, tech=tech, character=request.user)

    if r.state < STATE_CONCLUSION:
        messages.error(request, "You can't publish that research, you haven't finished it yet!!")
        return HttpResponseRedirect("/research/")

    pub = request.POST.get('publish', '')
    if pub:
        tech.publishedBy = request.user
        tech.save()
        request.user.save()
        r.state = STATE_PUBLISHED
        r.time = datetime.now()
        r.save()
        request.user.save()
        ALOG(request, "published %s!" % tech.name,  "published %s!" % tech.name)
        messages.success(request, "You published a tech!")
        return HttpResponseRedirect("/research/")
    
    return render_to_response("publish.html", {'tech':tech}, context_instance=RequestContext(request))


@login_required
def research_overview(request):
    started = Research.objects.filter(character=request.user, state__lt=STATE_CONCLUSION)
    done = Research.objects.filter(character=request.user, state__gte=STATE_CONCLUSION)



    return render_to_response("techoverview.html", {'started':started,'done':done,'published':published}, context_instance=RequestContext(request))

@login_required
def published(request):
    published = Research.objects.filter(state=STATE_PUBLISHED)
    tlevel = sum(map(lambda x: x.tech.difficultyLevel(), list(published)))

    return render_to_response("published.html", {'published':published, 'tlevel':tlevel}, context_instance=RequestContext(request))


@login_required
def unlock(request):
    techid = request.GET.get('tech','')
    if techid:
        if Tech.objects.filter(finishCode__iexact=techid).exists():
            tech = Tech.objects.get(finishCode__iexact=techid)
            if not tech in request.user.tech.all():
                research = Research(tech=tech, character=request.user, state=STATE_CONCLUSION)
                research.save()
            research = Research.objects.get(tech=tech,character=request.user)
            if research.state < STATE_CONCLUSION:
                research.state = STATE_CONCLUSION
                research.save()
            messages.success(request, "Success!  You unlocked %s as a completed tech." % tech.name)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER',"/research/"))
        tech = get_object_or_404(Tech, startCode__iexact=techid)
        if tech in request.user.tech.all():
            messages.error(request, "You already know about that, Doctor!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER',"/research/"))

        if not tech.is_published():
            for pt in tech.prereqs.all():
                if not (request.user.has_completed_tech(pt.startCode) or pt.is_published()):
                    #messages.success(request, "test!")
                    GLOG(request, "couldn't unlock tech %s (prereqs)" % tech.name)
                    return render_to_response("unlock.html", {'tech':tech, 'ptechs':tech.prereqs.all()}, context_instance=RequestContext(request))


        research = Research(tech = get_object_or_404(Tech, startCode=techid), character=request.user, state=STATE_HYPOTHESIS)
        research.save()
        messages.success(request, "Eureka!  You may be on to something here, Doctor!")
        PLOG(request, "started research on %s." % research.tech.name)
        return HttpResponseRedirect("/research/"+techid)
    
    return render_to_response("unlock.html", {'tech':None,'ptechs':None}, context_instance=RequestContext(request))


@login_required
def theorize(request):
    tech = None
    techname = request.GET.get('tech','')
    if techname:
        techs = Tech.objects.filter(name__iexact=techname) # Case-insensitive match.
        if len(techs):
            tech = techs[0]
            PLOG(request, "discovered a code for %s: %s." % (tech.name, tech.startCode))
        else:
            tech = None
        
    return render_to_response("theorize.html", {'tech':tech}, context_instance=RequestContext(request))


@login_required
def research(request, techid, startstate):

    can = True
    research = Research.objects.filter(tech__startCode = techid, character=request.user)
    if not len(research):
        research = Research(tech = get_object_or_404(Tech, startCode=techid), character=request.user, state=STATE_HYPOTHESIS)
        research.save()
    else:
        research = research[0]

    ss = int(startstate)

    if research.state < ss - 1:
        messages.error(request, "Your research has not progressed that far, Doctor!") 
        GLOG(request, "Research not far enough %s < %s" % (research.state, str(ss)))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER',"/research/"))
    elif ss == STATE_ANALYSIS:
        can = (research.tech.cost() <= request.user.computrons)

    children = []
    for nt in Tech.objects.all():
        if research.tech in nt.prereqs.all():
            children += [nt]

    if request.method == 'POST':
        if ss < research.state:
            messages.error(request, "Your research has moved beyond that, Doctor! Why repeat work?") 
            GLOG(request, "Research too far")
            return HttpResponseRedirect("/research/%s/%s" % (techid, str(research.state)))
        elif ss == STATE_HYPOTHESIS:
            PLOG(request, "began research on %s." % (research.tech.name))
        elif ss == STATE_DESIGN:
            PLOG(request, "designed an experiment for %s." % (research.tech.name))
        elif ss == STATE_EXPERIMENT:
            PLOG(request, "completed an experiment %s." % (research.tech.name))
        elif ss == STATE_ANALYSIS:
            request.user.computrons -= research.tech.cost()
            request.user.save()
            PLOG(request, "Spent %s computrons on %s" % (str(research.tech.cost()), research.tech.name))
            

        research.state = ss + 1
        research.save()
        ss = ss + 1



        return HttpResponseRedirect("/research/%s/%s" % (techid, str(ss)))
    else:
        further = (ss < research.state)
        ss = min(ss, research.state)
        done = (research.state >= STATE_CONCLUSION and ss >= STATE_CONCLUSION)
        prev = (ss - 1)
        next = (ss + 1)
        return render_to_response("science.html", {'further': further,'done':done,'prev':prev,'r':research, 'state':ss, 'can':can, 'children': children, 'next':next}, context_instance=RequestContext(request))

