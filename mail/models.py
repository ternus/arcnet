from django.db import models
from django.forms import ModelForm
from django import forms
from time import time

from django.utils import timesince

from core.models import *
from cyber.models import *

# Create your models here.

class Mail(models.Model):
    '''A message from one character to another.'''
    subject = models.CharField(max_length=200)
    sender = models.ForeignKey(Character, related_name="mail_sender", blank=True,null=True)
    recipient = models.ForeignKey(Character, related_name="mail_recipient", blank=False)
    time = models.DateTimeField(auto_now_add=True,editable=True)
    readtime = models.DateTimeField(blank=True,null=True)
    anonymous = models.BooleanField(default=False)
    text = models.TextField()

    @property
    def rsender(self):
        if self.anonymous:
            return "Anonymous"
        else:
            return self.sender

    def unread(self):
        return (self.readtime is None)

    def timesince(self):
        return timesince.timesince(self.time)

    def isoformat(self):
        return self.time.isoformat()

    def recipients(self):
        rstr = ""
        for r in self.recipient.all():
            rstr += str(r)
        return rstr

    def __unicode__(self):
        return self.sender.charname + "/" + self.recipient.charname + "/" + self.subject

    class Meta:
        
        ordering = ['-time']
    
class MailForm(ModelForm):
    class Meta:
        fields = ('subject', 'recipient', 'anonymous', 'text')
        model = Mail
        

def mail_gms(request, subject, text):
    m = Mail(subject=subject,sender=request.user,recipient=Character.objects.get(username='gm'),text=text)
    m.save()
