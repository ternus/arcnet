from django.db import models

# Create your models here.


from django.contrib import messages

GM      = 1
PRIVATE = 2
PUBLIC  = 3

class Event(models.Model):
    character = models.ForeignKey('core.Character', blank=True)
    request = models.TextField(blank=True)
    tochar = models.CharField(max_length=400, blank=True,null=True)
    toall = models.CharField(max_length=400,blank=True,null=True)
    time = models.DateTimeField(auto_now_add=True)
    priority = models.IntegerField(default=GM)

    def __unicode__(self):
        return "%s : %s : %s" % (self.time, self.character.charname, self.tochar)

    def visible(self):
        ''' Visible to users. '''
        return self.priority >= VISIBLE_PRIORITY

def LOG(priority, request, tochar, toall=None):
    e = Event(character=request.user,request=str(request),tochar=tochar,toall=toall,priority=priority)
    e.save()

def GLOG(request, tochar):
    LOG(GM, request, tochar)

def PLOG(request, tochar):
    LOG(PRIVATE, request, tochar)

def ALOG(request, tochar, toall):
    LOG(PUBLIC, request, tochar, toall)

def TLOG(user, tochar):
    e = Event(priority=PRIVATE, character=user, tochar=tochar)
    e.save()

def NLOG(toall):
    e = Event(toall=toall, priority=PUBLIC)
    e.save()
