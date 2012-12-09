from django.db import models
from random import *
from string import upper
from arcnet.core.models import *
from defaults import *

def gen_random_code():
    return upper(str(hex(randint(65536,1048575)))[2:])

class Tech(models.Model):
    name = models.CharField(max_length=200)
    tree = models.CharField(max_length=1, default='O')
    prereqs = models.ManyToManyField('Tech', symmetrical=False, related_name='techprereqs', blank=True)
    startCode = models.CharField(max_length=5, primary_key=True, unique=True, default=gen_random_code)
    finishCode = models.CharField(max_length=5, unique=True, default=gen_random_code)
    publishedBy = models.ForeignKey('core.Character', blank=True, null=True, related_name="tech_publisher")
    design = models.TextField(blank=True)
    experiment = models.TextField(blank=True)

    def __unicode__(self):
        return "L%s-%s %s %s" % (self.difficultyLevel(), self.tree, self.startCode, self.name) 

    def box(self):
        bstr = "\\n".join(self.__unicode__().split(" "))
        if (self.is_published()):
            bstr += "\\n(%s et al.)" % (self.publishedBy.charname.split(" ")[-1])
        return bstr

    def difficultyLevel(self):
        ''' Determines the difficulty level of a given question by
        recursively counting its prerequisites.'''

        if (len(self.prereqs.all()) == 0):
            return 1
        else:
            return reduce(lambda x, y: max(x,y), map(lambda x: x.difficultyLevel(), self.prereqs.all())) + 1

    def cost(self):
        return (self.difficultyLevel() * 3)

    def has_prereqs(self):
        return len(self.prereqs.all())

    def is_published(self):
        return (not (self.publishedBy is None))

    class Meta:
        ordering = ['name']

class Research(models.Model):
    ''' This is a throughput model from Character to Tech.'''
    time = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(default=0, choices=STATE_CHOICES)
    character = models.ForeignKey('core.Character')
    tech = models.ForeignKey(Tech)

    def __unicode__(self):
        return "%s : %s : %s" % (str(self.character), str(self.tech), research_states[self.state])

    def txtstate(self):
        return research_states[self.state]

    def complete(self):
        return self.state >= STATE_CONCLUSION
