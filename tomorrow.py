from media.models import *
from cyber.models import *

def tomorrow():

    for agent in Agent.objects.all():
        agent.endorsements_today = 0
        print agent
        agent.save()

    for computer in Computer.objects.all():
        if computer.auto_ice:
            computer.regenICE()
            computer.save()
            print computer

    for character in Character.objects.all():
        print character
        character.computrons = character.computron_income
        character.save()
        for access in character.access_set.all():
            if access.permanent == False:
                access.icelevel = 0
                access.save()

    print  "Done."

tomorrow()
