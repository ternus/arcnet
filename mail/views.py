# Create your views here.

from django import forms
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render_to_response, get_object_or_404

from models import *
from core.models import *
from elog.models import *
from datetime import datetime

@login_required
def allmail(request):
    mails = Mail.objects.filter(recipient=request.user)  # Fetch all mails for this user
    return render_to_response('allmail.html', {'mails':mails,}, context_instance=RequestContext(request))

@login_required
def sentmail(request):
    sentmail = Mail.objects.filter(sender=request.user)  # Fetch all mails for this user
    return render_to_response('sentmail.html', {'sentmail':sentmail}, context_instance=RequestContext(request))


@login_required
def readmail(request, mid):
    mail = get_object_or_404(Mail, id=mid)
    if (mail.sender != request.user) and (mail.recipient != request.user) and (not request.user.is_superuser):
        print mail.recipient, request.user
        messages.error(request, "Please don't try to view other people's mail!  (Logged for GM review.)")
        GLOG(request, "Tried to view mail belonging to %s (id %s)" % (mail.sender.charname, mail.id))
        return HttpResponseRedirect("/mail/")
    if not mail.readtime:
        mail.readtime = datetime.now()
        mail.save()
    return render_to_response('readmail.html', {'mail':mail}, context_instance=RequestContext(request))

@login_required
def sendmail(request):
    if request.method == 'POST':
        form = MailForm(request.POST)
        if form.is_valid():
            mail = form.save(commit=False)
            mail.sender = request.user
            if mail.anonymous and request.user.computrons <= 0:
                    messages.error(request, "You don't have enough computrons!")
                    GLOG(request, "tried to send mail but didn't have enough computrons.")
            else:
                if mail.anonymous:
                    request.user.computrons -= 1
                    request.user.save()
                mail.save()
                messages.success(request, "Mail sent!")
                PLOG(request, "sent mail to %s, subject %s." % (mail.recipient.charname, mail.subject))
                TLOG(mail.recipient, "got mail from %s, subject %s." % ( mail.rsender, mail.subject))
                return HttpResponseRedirect("/mail/")
        else:
            messages.error(request, "Something went wrong!")

    form = MailForm()
    to = request.GET.get('to','')
    if to:
        form.fields['recipient'].initial=Character.objects.get(username=to).id
    subj = request.GET.get('subj','')
    if subj:
        if subj[:3] == "Re:":
            form.fields['subject'].initial= subj
        else:
            form.fields['subject'].initial= "Re: "+subj
#        theirset = Character.objects.exclude(id=request.user.id)
#        form.fields['recipient'].queryset = theirset
    return render_to_response('sendmail.html', {'form':form}, context_instance=RequestContext(request))
            
