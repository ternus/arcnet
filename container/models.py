from django.db import models

# Create your models here.

class FileContainer(models.Model):

    def __unicode__(self):
        try:
            return self.character.__unicode__()
        except:
            try:
                return self.computer.__unicode__()
            except:
                try:
                    return self.mail.__unicode__()
                except:
                    return "unknown"

    class Meta:
        abstract = False
