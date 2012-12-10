from datetime import date
from django.db import models
from django.contrib.auth.models import User, UserManager
from django.utils import timesince

from defaults import *
from cyber.defaults import *
from cyber.models import *
from research.models import *
from research.defaults import *
from elog.models import *
import settings


class Character(User):
    """
    Represents an Arcadia character.

    NOTE: This is a hack.  Read this first: 
    http://scottbarnham.com/blog/2008/08/21/extending-the-django-user-model-with-inheritance/
    """

    playername = models.CharField(max_length=40, blank=True)
    nickname = models.CharField(max_length=40, blank=True)
    title = models.CharField(max_length=40, blank=True)

    #charname = models.CharField(max_length=40, unique=True)
    #title = models.CharField(max_length=40, blank=True, help_text="e.g. Doctor, Colonel")

    gender = models.CharField(max_length=13, choices=GENDER_CHOICES,default='Male')
    dob = models.DateField(default=DEFAULT_BIRTHDAY,blank=True)
    race = models.CharField(max_length=15, choices=RACE_CHOICES,default='Human')
    residence = models.CharField(max_length=20, choices=RESIDENCE_CHOICES, default='Arcadia')
    image = models.ImageField(upload_to="netimg/profiles/", blank=True)
    visible = models.BooleanField(default=True, help_text="Shows up in public rankings.")
    real = models.BooleanField(default=True)

    # FAME/PRESS  ################

    candidate = models.BooleanField(default=False)
    press = models.BooleanField(default=False)
    fame = models.PositiveIntegerField(default=0)
    buzz = models.PositiveIntegerField(default=0)

    readtime = models.DateTimeField(blank=True,null=True)

    # HACKING     ################

    #cur_persona = models.OneToOneField("Persona", blank=True,null=True) 

    hacker = models.BooleanField(default=True)
    computrons = models.IntegerField(default=0)
    computron_income = models.IntegerField(default=0, help_text="Computrons received per day.")

    computers = models.ManyToManyField('cyber.Computer', related_name='computers_seen', blank=True, through='cyber.Access')


    # PLAYER INFO ################

    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default='Active')
    type = models.CharField(max_length=10, choices=CHARTYPE_CHOICES,default='PC')
    phone = models.CharField(max_length=20, blank=True)
    donotcall = models.CharField(max_length=80, blank=True, default="N/A") 

    objects = UserManager()

    # Research
    tech = models.ManyToManyField('research.Tech', related_name='char_tech', blank=True, through='research.Research')
    
    class Meta:
        permissions = (
            ("is_auto", "Is automata"),
            ("is_press", "Member of the Press"),
            ("is_famous", "Candidate for Cultural Ambassador"),
            ("is_hacker", "Hacker"),
            )
        ordering = ['type', 'last_name']

    @property
    def charname(self):
        return self.first_name + " " + self.last_name

    @property
    def formalname(self):
        if self.title:
            return self.title + " " + self.last_name
        else:
            return self.charname

    @property
    def displayname(self):
        if self.nickname:
            if self.title:
                return self.title + " \"" + self.nickname + "\" " + self.last_name
            else:    
                return self.first_name + " \"" + self.nickname + "\" " + self.last_name
        else:
            return self.formalname

    @property
    def fullname(self):
        if self.nickname:
            return self.title + " " + self.first_name + " \"" + self.nickname + "\" " + self.last_name
        else:
            return self.title + " " + self.first_name + " " + self.last_name

    MAXWIDTH=245.0

    def idim(self, mw, mh=None):
        if not self.image:
            return ""
        w = self.image.width
        h = self.image.height
        ar = (float(w)/float(h))
        if (w > mw):
            sf = (float(mw)/float(w))
            h = int(h * sf)
            w = mw
        if mh:
            if (h > mh):
                sf = (float(mh)/float(h))
                w = int(w * sf)
                h = int(mh)
        ar = (float(w)/float(h))
        if (w < h):
            return (int(w), min(h, int(float(h)/ar)))
        return (int(w), max(h, int(float(h) / ar)))
            

    def iwidth(self, mw=MAXWIDTH, mh=None):
        return self.idim(mw, mh)[0]

    def iheight(self, mw=MAXWIDTH, mh=None):
        return self.idim(mw, mh)[1]

    def diheight(self):
        return (self.iheight()/ 2) - 35

    def imgstr(self, mw=MAXWIDTH,mh=None):
        if self.image:
            s = ("src='%s' width='%s' height='%s'" % (str(self.image.url), 
                                                      str(self.iwidth(mw,mh)), 
                                                      str(self.iheight(mw,mh))
                                                      ))

            return s
        else:
            return ("src='%s' width='%s' height='%s'" % (settings.MEDIA_URL+"/img/unknown.gif", mw, mh))

    def tinypic(self):
        return self.imgstr(70, 70)

    def chardiv(self):
        return "<div class=\"chardiv\"><a href='/char/%s'><img %s /> %s </a></div>" % (self.username, self.tinypic(), self.displayname)

    def charspan(self):
        return "<a href='/char/%s'><img %s /> %s </a>" % (self.username, self.tinypic(), self.displayname)

    def inventory(self):
        return self.cyberfile_set.all()

    def __unicode__(self):
        return self.charname

    def isPC(self):
        return (self.type != 'NPC')

    def lastlog(self):
        return timesince.timesince(self.last_login)

    def ranking(self, orderby):
        co = Character.objects.all().order_by(orderby)
        ranking = 1
        for c in co:
            if c == self:
                break
            ranking += 1
        return ranking

    def clink(self):
        return ("<a href='/char/%s'>%s</a>" % (self.username, self.displayname))

    def persona_set(self):
        return self.persona_set.all()
    
    def fame_ranking(self):
        co = Character.objects.all().filter(candidate=True).order_by('-fame')
        ranking = 1
        for c in co:
            if c == self:
                break
            ranking += 1
        return ranking

    def tied(self):
        return Character.objects.exclude(id=self.id).filter(fame=self.fame,candidate=True).exists()


    def buzz_ranking(self):
        return self.ranking('-buzz')

    def has_broken_ice(self, computer, layer):
        return (computer in self.computers.all() and Access.objects.get(computer=computer, character=self).icelevel > layer)

    def has_access(self, computer):
        if (computer in self.computers.all()):
            return Access.objects.get(computer=computer,character=self).has_access()
        else:
            return False

    def in_favorites(self, computer):
        return (computer in self.computers.all())

    def has_new_mail(self):
        return (self.new_mail() > 0)

    def new_mail(self):
        return len(self.mail_recipient.filter(readtime=None))

    def has_completed_tech(self, techid):
        try:
            return (Research.objects.get(character=self,tech__startCode=techid).state >= STATE_CONCLUSION)
        except:
            return False 

    def published(self):
        print self.tech.filter(research__state=STATE_PUBLISHED).all()
        return self.tech.filter(research__state=STATE_PUBLISHED).all()

    def tiedstr(self):
        if self.tied():
            return "(tied)"
        else:
            return ""

    def new_feeds(self):
        if self.readtime:
            return len(Event.objects.filter(time__gt=self.readtime, priority=PUBLIC))
        return len(Event.objects.filter(priority=PUBLIC))


    def has_new_events(self):
        return (self.new_feeds() > 0)
    

def get_characters():
    return Character.objects.all()
