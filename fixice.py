#!/usr/bin/env python

from cyber.models import *

for comp in Computer.objects.all():
	if len(comp.ice.all()) == 0:
		comp.regenICE()
		print comp

