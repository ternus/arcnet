from django.db import models
from django.forms import ModelForm
from django import forms
#from tinymce.widgets import TinyMCE

# Create your models here.

from core.models import *

class FameItem(models.Model):
    name = models.CharField(max_length=200)
    value = models.IntegerField(default=1)
    def __unicode__(self):
        return self.name + " (" + str(self.value) + "pt)"

class Post(models.Model):
    author = models.ForeignKey(Character, blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    characters = models.ManyToManyField(Character, related_name='characters_posts',blank=True)
    subject = models.CharField(max_length=255)
    image = models.ImageField(upload_to="netimg/", blank=True,null=True)
    text = models.TextField(blank=True,null=True)
    fameItems = models.ManyToManyField(FameItem, related_name='post_fame',blank=True)
    audio = models.FileField(upload_to="netimg/", blank=True,null=True)

    sinkers = models.ManyToManyField(Character, related_name='post_sink',blank=True,null=True)
    swimmers = models.ManyToManyField(Character, related_name='post_swim',blank=True,null=True)

    def notable(self):
        return len(self.fameItems.all())

    def timesince(self):
        return timesince.timesince(self.time)

    def __unicode__(self):
        return self.author.charname + " : " + self.subject

    def firstline(self):
        return (self.text)[:100]

    def istext(self):
        return (not (self.isaudio() or self.isimage()))

    def isimage(self):
        try:
            f = self.image.file
            return True
        except:
            return False

    def isaudio(self):
        try:
            f = self.audio.file
            return True
        except:
            return False

    def ss_score(self):
        return len(self.swimmers.all()) - len(self.sinkers.all())

    class Meta:
        ordering = ['-time']

class PostForm(ModelForm):
    characters = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                                queryset=Character.objects.all(),required=False)
    class Meta:
        fields = ('subject', 'text', 'characters')
        model = Post

class ImagePostForm(ModelForm):
    fameItems = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                               queryset=FameItem.objects.all(), required=False)
    characters = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                                queryset=Character.objects.all(),required=False)
    class Meta:
        fields = ('subject','image','text','fameItems','characters')
        model = Post

class AudioPostForm(ModelForm):
    characters = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                                queryset=Character.objects.all(),required=False)
    class Meta:
        fields = ('subject', 'audio','text','characters')
        model = Post


POSITION_CHOICES = (

    (1, "Support"),
    (-1, "Oppose")
    )

POSITION_STATES = {
#    0 : "Neutral",
    1 : "Support",
    -1 : "Oppose"
}

class Agent(models.Model):
    name = models.CharField(max_length=100)
    influence = models.IntegerField(default=1)
    controller = models.ForeignKey(Character)
    endorsements_today = models.IntegerField(default=0)
    endorsements = models.ManyToManyField('Subject', through='Position')
    candidate = models.ForeignKey(Character, blank=True, related_name="ca_candidate", null=True)
    direct = models.BooleanField(default=False, help_text="Set this to True if this directly represents a character.")
    
    
    def __unicode__(self):
        return self.name

TYPES = (
    ('s', 'Society'),
    ('e', 'Entity'),
    ('o', 'Other')
)

class Subject(models.Model):
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=1, default='s', choices=TYPES)
    pro = models.CharField(max_length=200,blank=True)
    anti = models.CharField(max_length=200,blank=True)
    starting_value = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

    def pbar(self):
        return int(385 * (float(100 + self.support())/200.0))

    def issociety(self):
        return (self.type == 's')


    def support(self):

        s = self.starting_value
        for position in self.position_set.all():
            s += (position.agent.influence * position.state)
        for factor in self.factor_set.all():
            s += factor.value
        return min(100, max(-100, s))

    def supporttext(self):
        s = self.support()
        r = ""
        if (abs(s) < 10):
            return "neutral"
        if (abs(s) < 25):
            r += "slightly "
        elif (abs(s) < 50):
            r += "leaning "
        elif (abs(s) < 75):
            r += "strongly "
        else:
            r += "overwhelmingly "
        if self.type == 's':
            if (s < 0):
                return r + "Con"
            else:
                return r + "Pro"
        elif self.type == 'e':
            if (s < 0):
                return r + "negative"
            else:
                return r + "positive"
        elif self.type == 'o':
            if (s < 0):
                return r + "against"
            else:
                return r + "in favor"



class Position(models.Model):
    state = models.IntegerField(default=0, choices=POSITION_CHOICES)
    agent = models.ForeignKey(Agent)
    subject = models.ForeignKey(Subject)
    time = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.agent.__unicode__() + " - " + POSITION_STATES[self.state] + " - " + self.subject.__unicode__()

    def tstate(self):
        return POSITION_STATES[self.state]

class Factor(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField(default=1)
    subject = models.ForeignKey(Subject)
    time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s - %s - %s" % (str(self.subject), self.name, str(self.value))

    def positive(self):
        return (self.value > 0)

class EndorseForm(ModelForm):
    class Meta:
        fields = ('agent', 'state', 'subject')
        model = Position

class CandidateForm(forms.Form):
    agent = forms.ChoiceField()#widget=forms.RadioSelect)
    candidate = forms.ChoiceField()#widget=forms.RadioSelect)

