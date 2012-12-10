from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from pythonsudoku.config import *
from pythonsudoku.sudoku import *
from pythonsudoku.board import *
from pythonsudoku.image import *

from defaults import *
from arcnet.settings import *
from random import *
from wordsearch import gen_wordsearch
from hashlib import md5
import core

class Rumor(models.Model):
    subject = models.CharField(max_length="100")
    text = models.TextField()

    def __unicode__(self):
        return self.subject

class Word(models.Model):
    word = models.CharField(max_length=100, unique=True,primary_key=True)
    level = models.IntegerField(choices=DLEVEL_CHOICES,default=DLEVEL_EASY)

    def __unicode__(self):
        return self.word

    class Meta:

        ordering = [ 'word' ]

class Picture(models.Model):
    image = models.ImageField(upload_to="netimg/trails/", blank=True,null=True)
    location = models.CharField(max_length=100, blank=True)
    level = models.IntegerField(choices=DLEVEL_CHOICES,default=DLEVEL_EASY)
    
    def __unicode__(self):
        return diff_levels[ self.level ] + "/" + self.location

    class Meta:
        ordering = [ 'location' ]



class Trance(models.Model):
    name = models.CharField(max_length=50)
    level = models.IntegerField(default=1)
    effects = models.TextField()

    def __unicode__(self):
        return self.name
    
    @property
    def caption(self):
        return self.effects

    @property
    def heading(self):
        return self.name


class ICE(models.Model):
    ice_type = models.CharField( max_length=1, choices=ICE_TYPES, default=SOCIAL_ENGINEERING )
    level = models.IntegerField( choices=SECURITY_CHOICES, default=MIN_LEVEL )
    seed = models.IntegerField( default=get_seed,unique=True,primary_key=True ) # Possible future bug, but I don't care.

    class Meta:
        ordering = ['level', 'ice_type', 'seed']

    def __unicode__(self):
        return str(self.ice_type) + ":" + str(self.level) + ":" +self.get_difficulty_str() + ":" + str(self.seed)

    def cost(self):
        return max(1, int(self.level))

    def save(self):
        if self.ice_type == BLOCK_CIPHER:
            s = Sudoku(Board(), difficulty=self.get_difficulty_str(), seed=self.seed)
            s.create()
            i = Image(s.to_board(), AUTOGEN_MEDIA_ROOT+'sudoku/'+str(self.seed)+'.png')
        super(ICE, self).save()

    def get_difficulty(self):
        seed(self.seed)
        return int( min( DLEVEL_HARD, max( DLEVEL_EASY, normalvariate( self.level + 1, LEVEL_SIGMA )  * CONVERSION_FACTOR ) ) )
        
    def get_difficulty_str(self):
        return diff_levels[ self.get_difficulty() ]

    def get_level(self):
        return levels[self.level]

    def get_real_type(self):
        return icetypes[self.ice_type]

    def get_type(self):
        if (self.ice_type != LINK_HIJACK):
            return self.get_real_type()
        myicetypes = icetypes.keys()
        myicetypes.remove(LINK_HIJACK)
        seed( self.seed )
        return icetypes[ choice( myicetypes ) ]

    def get_words(self):
        if not (self.ice_type == MEMORY_ANALYSIS or self.ice_type == SOCIAL_ENGINEERING):
            return []
        seed( self.seed )
        words = map(lambda x: x.__unicode__(), list(Word.objects.all()))
        return sample(words, self.level * 3)

    def get_image(self):
        if not (self.ice_type == PHYSICAL_ACCESS):
            return ""
        images = Picture.objects.filter( level = self.get_difficulty() )
        seed( self.seed )
        img = choice( images )
        return img
        

    def get_help(self):
        if self.ice_type in PRINTABLES:
            return helptexts[ self.ice_type ] + CAN_PRINT
        else:
            return helptexts[ self.ice_type ]

    def get_trance(self):
        trances = Trance.objects.all()
        seed( self.seed )
        return choice( trances )

    def get_people(self):
        people = core.models.Character.objects.filter( status='Active', real=True,visible=True )
        seed( self.seed )
        return sample( people, (12-self.level) )

    def render(self):
        mstr = ""
        if (self.ice_type == BLOCK_CIPHER):
            mstr += "<img src='"+AUTOGEN_MEDIA_URL+"sudoku/"+str(self.seed)+".png' />"
        elif (self.ice_type == MEMORY_ANALYSIS):
            words = self.get_words()
            mstr += "<ul style='text-align: left;'>"
            for word in words:
                mstr += "<li>"+word+"</li>"
            mstr += "</ul>"
            mstr += "<pre>"+gen_wordsearch(words, self.seed)+"</pre>"
        elif (self.ice_type == SOCIAL_ENGINEERING):

            mstr += "<ul style='text-align: left;'>"
            for person in self.get_people():
                mstr += "<li>"+person.chardiv()+"</li>"
            mstr += "</ul>"

            mstr += "<ul style='text-align: left;'>"
            for word in self.get_words():
                mstr += "<li>"+word+"</li>"
            mstr += "</ul>"
        elif (self.ice_type == PHYSICAL_ACCESS):
            if self.get_image():
                mstr += "<img src=\""+self.get_image().image.url+"\" width=300px />"
            else:
                mstr += "[ You may freely skip this. ]"
        elif (self.ice_type == LINK_HIJACK):
            trance = self.get_trance()
            mstr += "This is " + trance.name + " trance.  Its effects (if you don't see a popup) are:"
            mstr += "<div class='conttext'>"+trance.effects+"</div>"
        return mstr
        

def genICE(level=MIN_LEVEL):
    level_points = level * AVERAGE_ICE_LAYERS
    min_level = max(level - 1, MIN_LEVEL)
    max_level = min(level + 1, MAX_LEVEL)
    ice_levels = []
    while (sum(ice_levels) < level_points):
        ice_levels += [randint(min_level, max_level)]
    ice = []
    myiceset = icetypes.keys()
    for ice_level in ice_levels:
        type = choice(myiceset)
        if type in ICE_MAX_ONE:
            myiceset.remove(type) # Max of one sudoku
        newice = ICE(ice_type=type,level=ice_level)
        newice.save()
        ice += [newice]        
    return ice


class Access(models.Model):
    computer = models.ForeignKey('Computer')
    character = models.ForeignKey('core.Character')
    time = models.DateTimeField(auto_now_add=True)
    permanent = models.BooleanField(default=False)
    icelevel = models.IntegerField(default=0)
    
    def __unicode__(self):
        return ("%s : %s : %s" % (self.character.charname, self.computer.name, self.time))

    def has_access(self):
        return self.permanent or (self.icelevel >= len(self.computer.ice.all()))

class Computer(models.Model):
    name = models.CharField(max_length=200,unique=True,primary_key=True)
    address = models.CharField(max_length=15,help_text="Format: XXX:XXX:XXX, auto-generated",unique=True,default=genRandomIP)
    security_level = models.IntegerField(choices=SECURITY_CHOICES,default=MIN_LEVEL)
    description = models.TextField(blank=True, help_text="Optional text associated with this machine.")
    auto_ice = models.BooleanField(default=True)
    ice = models.ManyToManyField(ICE, blank=True, help_text="WILL BE AUTO-GENERATED")
    links_to = models.ManyToManyField('Computer', blank=True, related_name="links_to")

    def __unicode__(self):
        return self.address + " (" +self.name + ")"

    def save(self):
        if self.auto_ice and len(self.ice.all()) == 0:
            self.regenICE()
        super(Computer, self).save()
    
    def linksto(self):
        return self.links_to.all()

    def regenICE(self):
        for myice in self.ice.all():
            myice.delete()
        for myice in genICE(self.security_level):
            self.ice.add(myice)

    def slevel(self):
        return levels[self.security_level]


