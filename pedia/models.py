from django.db import models

# Create your models here.

class Entry(models.Model):
    name = models.CharField(max_length=100, unique=True, primary_key=True)
    text = models.TextField()
 
    def __unicode__(self):
        return self.name

    def previous(self):
        entries = Entry.objects.all().order_by("name")
        for i in range(len(entries)):
            if (entries[i] == self):
                break
        if i > 0:
            return entries[i-1]
        return None

    def next(self):
        entries = Entry.objects.all().order_by("name")
        for i in range(len(entries)):
            if (entries[i] == self):
                break
        if i < len(entries) - 1:
            return entries[i+1]
        return None
