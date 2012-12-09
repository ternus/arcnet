# Create your views here.

from django import forms
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib import messages

from models import *
from elog.models import *
from datetime import datetime

@login_required
def mediafeed(request,start=0,end=20):
    media = Post.objects.all()[start:end]
    return render_to_response('media.html', {'media':media}, context_instance=RequestContext(request))

@login_required
def allmedia(request):
    media = Post.objects.all()
    return render_to_response('media.html', {'media':media}, context_instance=RequestContext(request))


@login_required
def readpost(request, pid):
    post = get_object_or_404(Post, id=pid)
    notable = len(post.fameItems.all())
    return render_to_response('readpost.html', {'post':post, 'notable':notable}, context_instance=RequestContext(request))

@login_required
def textpost(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request, "Posted!")
            ALOG(request, "<a href='/media/%s'>posted</a> to the <a href='/media/'>media feed</a>." % post.id, "<a href='/media/%s'>posted</a> to the <a href='/media/'>media feed</a>." % post.id)
            return HttpResponseRedirect("/media/")
    else:
        form = PostForm()        
    return render_to_response('makepost.html', {'form':form}, context_instance=RequestContext(request))

@login_required
def imagepost(request):
    if request.method == 'POST':
        form = ImagePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            fame = 0
            for item in post.fameItems.all():
                fame += item.value
            for char in post.characters.all():
#                if char.candidate:
                #char.fame += fame
                char.save()
            if request.user.press:
                #request.user.buzz += fame
                request.user.save()
            ALOG(request, "posted an image to the media feed.", "posted an image to the media feed.")
            messages.success(request, "Posted!")
            return HttpResponseRedirect("/media/")
    else:
        form = ImagePostForm()
        form.fields['image'].required = True
    return render_to_response('imagepost.html', {'form':form}, context_instance=RequestContext(request))


@login_required
def audiopost(request):
    if request.method == 'POST':
        form = AudioPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request, "Posted!")
            ALOG(request, "posted to Radio Free Arcadia.", "posted to Radio Free Arcadia.")
            return HttpResponseRedirect("/media/")
    else:
        form = AudioPostForm()
    return render_to_response('audiopost.html', {'form':form}, context_instance=RequestContext(request))

# Login not required
def famouspeople(request):
    people = Character.objects.filter(candidate=True).order_by("-fame")[:10]
    return render_to_response('famous.html', {'people':people}, context_instance=RequestContext(request))

def subject(request,sname):
    subject = get_object_or_404(Subject,name=sname)
    people = Position.objects.filter(subject=subject).exclude(state=0)
    return render_to_response('popsubject.html', {'subject':subject,'positions':people}, context_instance=RequestContext(request))

def allsupport(request):
    socsubjects = Subject.objects.filter(type='s').order_by("name")
    ensubjects = Subject.objects.filter(type='e').order_by("name")
    osubjects = Subject.objects.filter(type='o').order_by("name")

    return render_to_response('popsupport.html', {'socsubjects':socsubjects,'ensubjects':ensubjects,'osubjects':osubjects}, context_instance=RequestContext(request))

@login_required
def endorse(request):
    if (request.method == 'POST'):
        form = EndorseForm(request.POST)
        if form.is_valid():
            position = form.save(commit=False)
            cp = Position.objects.filter(agent=position.agent,subject=position.subject)
            if len(cp):
                if cp[0].state != position.state:
                    cp[0].delete()
                    messages.warning(request, "You changed your mind on %s!" % position.subject.name)
                else:
                    messages.warning(request, "You're already endorsing %s that way." % position.subject.name)
                    return HttpResponseRedirect("/opinion/")
            position.agent.endorsements_today += 1
            position.agent.save()
            

            position.save()

            if position.state < 0:
                supop = "denounced"
            else:
                supop = "supported"
            if position.agent.direct:
                ALOG(request, "%s %s." % (supop, position.subject.name), "%s %s." % (supop, position.subject.name))
            return HttpResponseRedirect("/opinion/")
        else:
            messages.error(request, "Fail")
    else:
        form = EndorseForm()

    form.fields['agent'].widget = forms.RadioSelect()
    form.fields['agent'].queryset = Agent.objects.filter(controller=request.user)
    agent = request.GET.get('agent','')
    if agent:
        form.fields['agent'].initial = Agent.objects.get(name=agent).id
    form.fields['agent'].initial= Agent.objects.get(controller=request.user,direct=True).id
    form.fields['agent'].choices = (
        (a.id, ("%s (made %s endorsements today)" % (a.name, a.endorsements_today))) for a in Agent.objects.filter(controller=request.user))
    form.fields['agent'].required=True
    form.fields['subject'].blank=False
    form.fields['subject'].empty_label = None
    form.fields['subject'].queryset = Subject.objects.order_by('name')
    subject = request.GET.get('subject','')
    if subject:
        form.fields['subject'].initial = Subject.objects.get(name=subject).id

    return render_to_response('endorse.html', {'form':form}, context_instance=RequestContext(request))    


@login_required
def candidate(request):
    if (request.method == 'POST'):
        agent = Agent.objects.get(id=int(request.POST.get('agent','')))
        newcandidate = Character.objects.get(id=int(request.POST.get('candidate','')))

        if agent.candidate:
            messages.warning(request, "You changed your candidate endorsement from %s to %s!" % (agent.candidate,newcandidate.charname))
            #agent.candidate.fame -= agent.influence
            #agent.candidate.save()
        agent.candidate = newcandidate
        #agent.candidate.fame += agent.influence
        agent.candidate.save()
        agent.save()
                
        if agent.direct:
            ALOG(request, "endorsed %s for Cultural Ambassador." % (agent.candidate.charname), "endorsed %s for Cultural Ambassador." % (agent.candidate.charname))
#        else:
            #NLOG("%s endorsed %s for Cultural Ambassador." % (agent.name, agent.candidate.charname))
        return HttpResponseRedirect("/opinion/")
        
    else:
        form = CandidateForm(auto_id=False)

#    form.fields['agent'].widget = forms.RadioSelect()
    achoices = (
        (a.id, ("%s (currently endorsing: %s)" % (a.name, a.candidate))) for a in Agent.objects.filter(controller=request.user))
    form.fields['agent'].widget = forms.RadioSelect()
    form.fields['agent'].queryset = Agent.objects.filter(controller=request.user)
    agent = request.GET.get('agent','')
    if agent:
        form.fields['agent'].initial = Agent.objects.get(name=agent).id
    form.fields['agent'].initial= Agent.objects.get(controller=request.user,direct=True).id
    form.fields['agent'].choices = achoices


    form.fields['candidate'].widget = forms.RadioSelect()
    form.fields['candidate'].queryset = Character.objects.filter(candidate=True,visible=True).order_by('name')
    form.fields['candidate'].choices = (( c.id, ("%s (ranked %s) %s" %(c.charname, c.fame_ranking(), c.tiedstr())) ) for c in Character.objects.filter(candidate=True,visible=True).order_by('fame').all())

    return render_to_response('candidate.html', {'form':form}, context_instance=RequestContext(request))    


@login_required
def agents(request):
    return render_to_response('popagent.html', {}, context_instance=RequestContext(request))    

@login_required
def homefeed(request):
    events = Event.objects.filter(priority=PUBLIC).order_by('-time')[:30]
#    request.user.readtime = datetime.now()
#    request.user.save()

    return render_to_response('home.html', {'events':events}, context_instance=RequestContext(request))

@login_required
def myfeed(request):
    events = Event.objects.filter(priority__gte=PRIVATE, character=request.user).order_by('-time')
    return render_to_response('mystuff.html', {'events':events}, context_instance=RequestContext(request))
