# Create your views here.

from django import forms
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import render_to_response, get_object_or_404
from arcnet.core.models import *
from elog.models import *
from models import *
from random import *
from mail.models import *

@login_required
def net_home(request):
    a = request.GET.get('address', '')
    if a:
        return HttpResponseRedirect("/net/"+a)
    return render_to_response("net.html", {}, context_instance=RequestContext(request))

@login_required
def hack_computer(request, addr):

    comp = get_object_or_404(Computer, address=addr)
    if request.user.has_access(comp):
        return HttpResponseRedirect("/net/"+addr+"/server")

    level = 0
    print request.user.computers.all()
    start = request.GET.get('start', '')
    i = comp.ice.all().order_by('seed')[0]
    if (Access.objects.filter(character=request.user, computer=comp).exists()):
        a = Access.objects.get(character=request.user, computer=comp)
        i = comp.ice.all().order_by('seed')[a.icelevel]
        level = a.icelevel
    elif start:
        if (request.user.computrons < comp.security_level):
            messages.error(request,"You don't have enough computrons to start hacking this computer!")
        else:
            a = Access(character=request.user,computer=comp)
            a.save()
            request.user.computrons -= comp.security_level
            request.user.save()
            messages.success(request,"You started hacking %s!" % comp.address)
    canthack = (request.user.computrons < comp.security_level)

    return render_to_response("hack.html", {'c':comp, 'ice':i, 'canthack':canthack, 'level': level}, context_instance=RequestContext(request))

@login_required
def access_computer(request, addr):
    comp = get_object_or_404(Computer, address=addr)
    if (request.method == 'POST'):
        what = request.POST.get('what','')
        if what:
            mail_gms(request, "Did something on computer " + comp.__unicode__(), what)

    if not request.user.has_access(comp):
        messages.error(request, "You don't have access to that computer!")
        return HttpResponseRedirect("/net/"+addr)
    return render_to_response("computer.html", {'c':comp}, context_instance=RequestContext(request))

@login_required
def full_ice(request, addr):
    comp = get_object_or_404(Computer, address=addr)
    ice = comp.ice.all()
    return render_to_response("fullice.html", {'c':comp, 'ice':ice}, context_instance=RequestContext(request))

@login_required
def render_ice(request, addr, iceid, layer):
    comp = get_object_or_404(Computer, address=addr)
    ice = get_object_or_404(ICE, seed=iceid)
    complete = request.GET.get('complete','')
    force = request.GET.get('force','')
    
    canforce = (request.user.computrons >= ice.cost())

    if not Access.objects.filter(character=request.user, computer=comp).exists():
        pass

    a = Access.objects.get(character=request.user, computer=comp)

    if a.icelevel > int(layer):
        messages.info(request, "You've already broken this level of ICE.")
        return HttpResponseRedirect("/net/"+addr)

    if force:
        if (canforce):
            request.user.computrons -= ice.cost()
            request.user.save()
            complete = True
        else:
            messages.error(request, "You don't have enough computrons for that!")
    if complete:
        a.icelevel += 1
        a.save()
        return HttpResponseRedirect("/net/"+addr)

    if request.user.has_broken_ice(comp, iceid):
        messages.info(request, "You've already broken this level of ICE.")
        return HttpResponseRedirect("/net/"+addr)

    trance = None
    if (ice.ice_type == LINK_HIJACK):
        trance = ice.get_trance()

    return render_to_response("ice-render.html", {'c':comp,'ice':ice, 'layer': layer, 'nextlayer': str(int(layer) + 1), 'canforce': canforce, 'trance':trance}, context_instance=RequestContext(request))

class TransferForm(forms.Form):
    user = forms.CharField(max_length=200)
    amount = forms.IntegerField()
    why = forms.CharField(max_length=200)


@login_required
def computrons(request):
    if request.method == 'GET':
        add = request.GET.get('add','')
        if add:
            request.user.computrons += int(add)
            request.user.save()
            # TODO log
            messages.success(request, "Added " + add + " computrons!")

    if request.method == 'POST':
        if Character.objects.filter(username=request.POST.get('user','')).exists():
            to = Character.objects.get(username=request.POST.get('user',''))
            amount = int(request.POST.get("amount", ""))
            if amount <= request.user.computrons:
                if amount >= 0:
                    request.user.computrons -= amount
                    request.user.save()
                    to.computrons += amount
                    to.save()
                    PLOG(request, "sent %s computrons to %s (reason: %s)." % (amount, to, request.POST.get('why')))
                    TLOG(to, "received %s computrons from %s (reason: %s)." % (amount, request.user, request.POST.get('why')))
                    messages.success(request, "Computrons transferred!")
                else:
                    GLOG(request, "tried to steal computrons!")
                    messages.error(request, "Don't steal computrons!")
            else:
                messages.error(request, "You don't have enough computrons!")
        else:
            messages.error(request, "No such user!")
    form = TransferForm()
    return render_to_response("computrons.html", {'form':form}, context_instance=RequestContext(request))


@login_required
def rumors(request):
    rumor = None
    if request.method == 'GET':
        type  = request.GET.get('type', '')
        if type:
            rumor = choice(Rumor.objects.all())
            if type == 'pay':
                if request.user.computrons <= 0:
                    return render_to_response("rumors.html", {'rumor':None}, context_instance=RequestContext(request))
                request.user.computrons -= 1
                request.user.save()
                PLOG(request, "heard a rumor about %s: \"%s\"." % (rumor.subject, rumor.text))

    return render_to_response("rumors.html", {'rumor':rumor}, context_instance=RequestContext(request))
