from models import *
from defaults import *

PROGRAMS = {
    'enhance'  : [ "Enhance!", LEVEL_GREEN, 
                   "Thanks to advanced zooming algorithms, you can analyze " +
                   "security footage and extract forensic data.  Enhance!" ],

    'mailgrep' : [ "Mail Search", LEVEL_GREEN,
                   "Search through mail passing through this machine and " +
                   "extract a random rumor." ],

    'bcdecode' : [ "Analyze Block Cipher", LEVEL_GREEN,
                   "Advanced analysis of block ciphers.  Reduces " +
                   "the cost of brute-forcing block ciphers by 1." ],

    'memsift'  : [ "Memory Analytics Tool", LEVEL_GREEN,
                   "Speeds the task of memory analysis by reducing " +
                   "the number of search strings." ],

    'spre4d3r' : [ "Industrial Espionage Rootkit", LEVEL_BLUE,
                   "Spreads sensitive corporate information, decreasing "+
                   "that corporation's Public Support." ],

    'bl4st3r'  : [ "Industrial Sabotage Rootkit", LEVEL_BLUE,
                   "Disrupts industrial processes, decreasing "+
                   "a corporation's invested resources." ],

    'FFFH4R3'  : [ "FFFH4R3", LEVEL_YELLOW, "???" ], # Wonderland access

    'TG_Bas'   : [ "TranceGuardian(TM) Basic", LEVEL_GREEN,
                   "Gives a small chance of being alerted to trance." ],

    'TG_Std'   : [ "TranceGuardian(TM) Standard", LEVEL_YELLOW,
                   "Gives a moderate chance of being alerted to trance." ],

    'TG_Pro'   : [ "TranceGuardian(TM) Pro", LEVEL_RED,
                   "Gives a high chance of being alerted to trance." ],

}

for i in range(MIN_LEVEL, MAX_LEVEL + 1):
    newprog = { 'brkice_'+levels[i] : [ "Decrypter: "+levels[i], i, 
                                        "Allows you to break " + levels[i] + "-level encryption." ] }
    PROGRAMS.update(newprog)

def init_programs():
    for p in PROGRAMS:
        cp = CyberProgram(bname=p, name=PROGRAMS[p][0], level=PROGRAMS[p][1], desc=PROGRAMS[p][2])
        cp.save()


